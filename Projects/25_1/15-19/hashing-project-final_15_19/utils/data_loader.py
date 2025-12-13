import os

def load_words(path):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    full_path = os.path.join(base_dir, path)

    words = []
    with open(full_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line != "":
                words.append(line)

    return words
