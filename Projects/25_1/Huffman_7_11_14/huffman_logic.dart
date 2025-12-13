import 'package:collection/collection.dart';
import 'dart:math';

class HuffmanNode implements Comparable<HuffmanNode> {
  final String? character;
  final int frequency;
  final HuffmanNode? left;
  final HuffmanNode? right;

  HuffmanNode(this.frequency, {this.character, this.left, this.right});

  bool get isLeaf => left == null && right == null;

  @override
  int compareTo(HuffmanNode other) => frequency.compareTo(other.frequency);
}

class HuffmanCoding {
  HuffmanNode? _root;
  final Map<String, String> _codes = {};
  final Map<String, String> _reverseCodes = {};

  void build(String text) {
    _codes.clear();
    _reverseCodes.clear();
    _root = null;

    if (text.isEmpty) return;

    final frequencies = <String, int>{};
    for (var char in text.split('')) {
      frequencies[char] = (frequencies[char] ?? 0) + 1;
    }

    // 2. Create Priority Queue
    final priorityQueue = PriorityQueue<HuffmanNode>();
    frequencies.forEach((char, freq) {
      priorityQueue.add(HuffmanNode(freq, character: char));
    });

    // 3. Build the Tree
    if (priorityQueue.length == 1) {
      final onlyNode = priorityQueue.removeFirst();
      _root = HuffmanNode(onlyNode.frequency, left: onlyNode, right: null);
    } else {
      while (priorityQueue.length > 1) {
        final left = priorityQueue.removeFirst();
        final right = priorityQueue.removeFirst();

        final parent = HuffmanNode(
          left.frequency + right.frequency,
          left: left,
          right: right,
        );
        priorityQueue.add(parent);
      }
      _root = priorityQueue.first;
    }

    _generateCodes(_root, "");
  }

  void _generateCodes(HuffmanNode? node, String currentCode) {
    if (node == null) return;

    if (node.isLeaf) {
      final code = currentCode.isEmpty ? "0" : currentCode;
      _codes[node.character!] = code;
      _reverseCodes[code] = node.character!;
      return;
    }

    _generateCodes(node.left, "${currentCode}0");
    _generateCodes(node.right, "${currentCode}1");
  }

  String encode(String text) {
    if (_codes.isEmpty) return "";
    return text.split('').map((char) => _codes[char]).join();
  }

  String decode(String encodedSequence) {
    if (_reverseCodes.isEmpty) return "";
    StringBuffer decodedText = StringBuffer();
    String temp = "";

    for (var bit in encodedSequence.split('')) {
      temp += bit;
      if (_reverseCodes.containsKey(temp)) {
        decodedText.write(_reverseCodes[temp]);
        temp = "";
      }
    }
    return decodedText.toString();
  }

  double calculateEntropy(String text) {
    if (text.isEmpty) return 0.0;

    final frequencies = <String, int>{};
    for (var char in text.split('')) {
      frequencies[char] = (frequencies[char] ?? 0) + 1;
    }

    final totalLength = text.length;
    double entropy = 0.0;

    frequencies.forEach((char, freq) {
      final probability = freq / totalLength;

      final log2Probability = (probability > 0)
          ? (log(probability) / log(2))
          : 0.0;

      entropy += probability * log2Probability;
    });

    return -entropy;
  }

  Map<String, String> get codeTable => _codes;
  HuffmanNode? get root => _root;
}
