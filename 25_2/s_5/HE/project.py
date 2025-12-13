from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, List, Tuple, Iterable
from collections import Counter
import heapq
import re

import numpy as np
from scipy.sparse import lil_matrix, csr_matrix
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfTransformer

import matplotlib.pyplot as plt  # ГРАФИКИ

# ======================================================
# 0. Токенизация
# ======================================================

WORD_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def tokenize(text: str) -> List[str]:
    """Простейший токенизатор: слова + знаки препинания, всё в lower."""
    return WORD_RE.findall(text.lower())


# ======================================================
# 1. Хаффман-дерево по словам
# ======================================================

@dataclass(order=True)
class HuffmanNode:
    freq: int
    token: Optional[str] = field(compare=False, default=None)
    left: Optional["HuffmanNode"] = field(compare=False, default=None)
    right: Optional["HuffmanNode"] = field(compare=False, default=None)


def build_frequency_table_tokens(tokens: Iterable[str]) -> Dict[str, int]:
    return dict(Counter(tokens))


def build_huffman_tree(freq_table: Dict[str, int]) -> HuffmanNode:
    heap: List[HuffmanNode] = [HuffmanNode(f, t) for t, f in freq_table.items()]
    heapq.heapify(heap)

    # Если только один уникальный токен
    if len(heap) == 1:
        node = heap[0]
        return HuffmanNode(node.freq, None, node, None)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = HuffmanNode(n1.freq + n2.freq, None, n1, n2)
        heapq.heappush(heap, merged)

    return heap[0]


def build_code_table_tokens(root: HuffmanNode) -> Dict[str, str]:
    """token -> битовая строка Хаффмана."""
    code: Dict[str, str] = {}

    def traverse(node: HuffmanNode, prefix: str) -> None:
        if node.token is not None:
            code[node.token] = prefix or "0"
            return
        if node.left:
            traverse(node.left, prefix + "0")
        if node.right:
            traverse(node.right, prefix + "1")

    traverse(root, "")
    return code


# ======================================================
# 2. Baseline word-tokenizer
# ======================================================

def baseline_word_tokenizer(corpus_texts: List[str], min_freq: int = 3) -> Dict[str, int]:
    """
    Строим базовый токенизатор: слово -> индекс.
    0 оставляем под PAD/UNK.
    min_freq — минимальная частота слова в train, чтобы попасть в словарь.
    """
    counts: Counter = Counter()
    for txt in corpus_texts:
        counts.update(tokenize(txt))

    vocab: Dict[str, int] = {}
    for tok, cnt in counts.items():
        if cnt >= min_freq:
            vocab[tok] = len(vocab) + 1  # 1..|V|
    return vocab


def baseline_encode(text: str, vocab: Dict[str, int]) -> List[int]:
    return [vocab.get(t, 0) for t in tokenize(text)]  # 0 = UNK


def prepare_dataset_baseline(
    texts: List[str],
    vocab: Dict[str, int],
) -> List[List[int]]:
    return [baseline_encode(t, vocab) for t in texts]


# ======================================================
# 3. Word-aligned Huffman tokenizer
# ======================================================

class WordAlignedHuffmanTokenizer:
    """
    Word-level Huffman: для каждого слова строим Хаффман-код,
    но при классификации слово остаётся 1 токеном.
    """

    def __init__(self, corpus_texts: List[str], unk_token: str = "<unk>"):
        self.UNK = unk_token

        # 1) Собираем все токены из корпуса
        all_tokens: List[str] = []
        for txt in corpus_texts:
            all_tokens.extend(tokenize(txt))

        # 2) Частоты
        freq_table = build_frequency_table_tokens(all_tokens)

        # 3) UNK для OOV-слов
        if self.UNK not in freq_table:
            freq_table[self.UNK] = 1

        self.freq_table = freq_table

        # 4) Дерево Хаффмана и таблица кодов (token -> bits)
        self.tree = build_huffman_tree(self.freq_table)
        self.code_table = build_code_table_tokens(self.tree)

        # 5) Словарь кодов: token -> целочисленный ID
        #    (ID можно присваивать в порядке увеличения длины кода)
        tokens_sorted = sorted(
            self.code_table.keys(),
            key=lambda t: (len(self.code_table[t]), self.code_table[t])
        )

        self.token_to_id: Dict[str, int] = {}
        for idx, tok in enumerate(tokens_sorted, start=1):
            self.token_to_id[tok] = idx

        self.vocab_size: int = len(self.token_to_id) + 1  # +1 для 0=PAD/UNK

    def encode(self, text: str) -> List[int]:
        """
        Текст -> последовательность целочисленных токенов.
        Каждый токен = одно слово, закодированное Хаффманом, но как 1 ID.
        """
        toks = tokenize(text)
        ids: List[int] = []
        unk_id = self.token_to_id.get(self.UNK, 0)
        for t in toks:
            ids.append(self.token_to_id.get(t, unk_id))
        return ids


def prepare_dataset_huffman_word(
    texts: List[str],
    huff_tok: WordAlignedHuffmanTokenizer,
) -> List[List[int]]:
    return [huff_tok.encode(t) for t in texts]


# ======================================================
# 4. Общая функция: seqs -> BOW
# ======================================================

def seqs_to_bow(seqs: List[List[int]], vocab_size: int) -> csr_matrix:
    """
    Bag-of-Tokens (частотный вектор) в виде разреженной матрицы.
    vocab_size = максимальный ID токена + 1.
    """
    X = lil_matrix((len(seqs), vocab_size), dtype=np.float32)
    for i, s in enumerate(seqs):
        for tok in s:
            if 0 <= tok < vocab_size:
                X[i, tok] += 1.0
    return X.tocsr()


# ======================================================
# 5. Датасет и сравнение
# ======================================================

def load_binary_text_dataset() -> Tuple[List[str], np.ndarray, List[str]]:
    """
    Берём 2 категории из 20newsgroups и получаем бинарный текстовый датасет.
    Возвращаем тексты, метки и имена классов.
    """
    categories = ["rec.autos", "rec.sport.hockey"]

    data = fetch_20newsgroups(
        subset="all",
        categories=categories,
        remove=("headers", "footers", "quotes"),
    )

    texts: List[str] = data.data
    labels: np.ndarray = data.target  # 0/1
    target_names: List[str] = data.target_names
    return texts, labels, target_names


def predict_text(
    text: str,
    vocab: Dict[str, int],
    huff_tok: WordAlignedHuffmanTokenizer,
    tfidf_base: TfidfTransformer,
    clf_base: LinearSVC,
    tfidf_huff: TfidfTransformer,
    clf_huff: LinearSVC,
    baseline_vocab_size: int,
    huffman_vocab_size: int,
    target_names: List[str],
) -> None:
    """
    Классификация одного предложения / текста.
    Печатаем предсказания baseline и Huffman.
    """

    # -------- Baseline ----------
    seq_base = baseline_encode(text, vocab)
    X_base_counts = seqs_to_bow([seq_base], baseline_vocab_size)
    X_base = tfidf_base.transform(X_base_counts)
    y_base = clf_base.predict(X_base)[0]
    label_base = target_names[y_base]

    # -------- Huffman ----------
    seq_huff = huff_tok.encode(text)
    X_huff_counts = seqs_to_bow([seq_huff], huffman_vocab_size)
    X_huff = tfidf_huff.transform(X_huff_counts)
    y_huff = clf_huff.predict(X_huff)[0]
    label_huff = target_names[y_huff]

    print("\n=== Предсказание для текста ===")
    print(text)
    print("--------------------------------")
    print(f"Baseline предсказал класс: {label_base} (label={y_base})")
    print(f"Huffman  предсказал класс: {label_huff} (label={y_huff})")


def run_classification_comparison_word_aligned() -> None:
    """
    Сравнение:
      1) Baseline word-индексы
      2) Word-aligned Huffman токены (одно слово = один токен),
         где IDs присвоены с учётом длины Хаффман-кода.
    Оба варианта используют BOW -> TF-IDF -> LinearSVC.

    Плюс: строим графики и даём возможность ввести свой текст.
    """
    texts, labels, target_names = load_binary_text_dataset()

    train_texts, test_texts, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    print(f"\nDataset sizes: train={len(train_texts)}, test={len(test_texts)}")
    print(f"Classes: {target_names}")

    # -------- Baseline --------
    vocab = baseline_word_tokenizer(train_texts, min_freq=3)
    train_seqs_base = prepare_dataset_baseline(train_texts, vocab)
    test_seqs_base = prepare_dataset_baseline(test_texts, vocab)

    baseline_vocab_size = len(vocab) + 1
    X_train_base_counts = seqs_to_bow(train_seqs_base, baseline_vocab_size)
    X_test_base_counts = seqs_to_bow(test_seqs_base, baseline_vocab_size)

    tfidf_base = TfidfTransformer()
    X_train_base = tfidf_base.fit_transform(X_train_base_counts)
    X_test_base = tfidf_base.transform(X_test_base_counts)

    clf_base = LinearSVC()
    clf_base.fit(X_train_base, y_train)
    y_pred_base = clf_base.predict(X_test_base)
    acc_base = accuracy_score(y_test, y_pred_base)

    # -------- Huffman word-aligned --------
    huff_tok = WordAlignedHuffmanTokenizer(train_texts)
    train_seqs_huff = prepare_dataset_huffman_word(train_texts, huff_tok)
    test_seqs_huff = prepare_dataset_huffman_word(test_texts, huff_tok)

    huffman_vocab_size = huff_tok.vocab_size
    X_train_huff_counts = seqs_to_bow(train_seqs_huff, huffman_vocab_size)
    X_test_huff_counts = seqs_to_bow(test_seqs_huff, huffman_vocab_size)

    tfidf_huff = TfidfTransformer()
    X_train_huff = tfidf_huff.fit_transform(X_train_huff_counts)
    X_test_huff = tfidf_huff.transform(X_test_huff_counts)

    clf_huff = LinearSVC()
    clf_huff.fit(X_train_huff, y_train)
    y_pred_huff = clf_huff.predict(X_test_huff)
    acc_huff = accuracy_score(y_test, y_pred_huff)

    # ----- длины последовательностей -----
    def avg_len(seqs: List[List[int]]) -> float:
        return sum(len(s) for s in seqs) / len(seqs)

    avg_len_base = avg_len(train_seqs_base)
    avg_len_huff = avg_len(train_seqs_huff)

    print("\n=== Classification comparison: Baseline vs Word-aligned Huffman ===")
    print(f"Baseline accuracy: {acc_base:.4f}")
    print(f"Huffman  accuracy: {acc_huff:.4f}")
    print(f"Average seq length (baseline train): {avg_len_base:.2f}")
    print(f"Average seq length (Huffman  train): {avg_len_huff:.2f}")
    print(f"Vocab size (baseline): {baseline_vocab_size}")
    print(f"Vocab size (Huffman):  {huffman_vocab_size}")

    # ==================================================
    # ГРАФИКИ
    # ==================================================

    # 1) График accuracy
    models = ["Baseline", "Huffman"]
    accuracies = [acc_base, acc_huff]

    plt.figure()
    plt.bar(models, accuracies)
    plt.ylabel("Accuracy")
    plt.title("Accuracy: Baseline vs Huffman (20 Newsgroups subset)")
    for i, v in enumerate(accuracies):
        plt.text(i, v + 0.001, f"{v:.3f}", ha="center", va="bottom")
    plt.ylim(0, 1.0)
    plt.show()

    # 2) График средних длин последовательностей
    avg_lengths = [avg_len_base, avg_len_huff]

    plt.figure()
    plt.bar(models, avg_lengths)
    plt.ylabel("Average sequence length (train)")
    plt.title("Average sequence length: Baseline vs Huffman")
    for i, v in enumerate(avg_lengths):
        plt.text(i, v + 0.1, f"{v:.1f}", ha="center", va="bottom")
    plt.show()

    # ==================================================
    # ИНТЕРАКТИВ: ввести предложение и классифицировать
    # ==================================================
    print("\nТеперь можно вводить свои предложения для классификации.")
    print("Классы:", target_names)
    print("Введите 'exit' или пустую строку для выхода.")

    while True:
        text = input("\nВведите предложение: ").strip()
        if text == "" or text.lower() in ("exit", "quit"):
            print("Выход из режима предсказаний.")
            break

        predict_text(
            text=text,
            vocab=vocab,
            huff_tok=huff_tok,
            tfidf_base=tfidf_base,
            clf_base=clf_base,
            tfidf_huff=tfidf_huff,
            clf_huff=clf_huff,
            baseline_vocab_size=baseline_vocab_size,
            huffman_vocab_size=huffman_vocab_size,
            target_names=target_names,
        )



if __name__ == "__main__":
    run_classification_comparison_word_aligned()
