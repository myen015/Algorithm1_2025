import 'package:flutter/material.dart';
import 'package:graphview/GraphView.dart';
import 'huffman_logic.dart';

import 'package:flutter/foundation.dart' show kIsWeb;
import 'dart:html' as html;
import 'dart:typed_data';

void main() {
  runApp(
    const MaterialApp(debugShowCheckedModeBanner: false, home: HuffmanApp()),
  );
}

class HuffmanApp extends StatefulWidget {
  const HuffmanApp({super.key});

  @override
  State<HuffmanApp> createState() => _HuffmanAppState();
}

class _HuffmanAppState extends State<HuffmanApp> {
  final TextEditingController _controller = TextEditingController();
  final TextEditingController _encodedController = TextEditingController();
  final HuffmanCoding _huffman = HuffmanCoding();

  String _encodedResult = "";
  String _decodedResult = "";
  double _shannonEntropy = 0.0;
  double _averageCodeLength = 0.0;

  final Graph _graph = Graph()..isTree = true;
  final BuchheimWalkerConfiguration _builder = BuchheimWalkerConfiguration();

  @override
  void initState() {
    super.initState();
    _builder
      ..siblingSeparation = (25)
      ..levelSeparation = (35)
      ..subtreeSeparation = (25)
      ..orientation = (BuchheimWalkerConfiguration.ORIENTATION_TOP_BOTTOM);
  }

  void _processInput(String text) {
    setState(() {
      _huffman.build(text);
      _encodedResult = _huffman.encode(text);

      if (text.isNotEmpty) {
        _shannonEntropy = _huffman.calculateEntropy(text);

        final totalBits = _encodedResult.length;
        _averageCodeLength = totalBits / text.length;
      } else {
        _shannonEntropy = 0.0;
        _averageCodeLength = 0.0;
      }

      _encodedController.text = _encodedResult;
      _decodedResult = text;

      _buildGraphDisplay();
    });
  }

  void _decodeInput(String encodedText) {
    setState(() {
      if (_huffman.root == null || _huffman.codeTable.isEmpty) {
        _decodedResult = "ERROR: Build tree first by entering text above.";
      } else if (encodedText.isEmpty) {
        _decodedResult = "";
      } else {
        _decodedResult = _huffman.decode(encodedText);
      }
    });
  }

  Future<void> _uploadAndEncode() async {
    if (!kIsWeb) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            "File upload is only implemented for Web using dart:html.",
          ),
        ),
      );
      return;
    }

    final input = html.FileUploadInputElement()..accept = '.txt';
    input.click();

    await input.onChange.first;

    if (input.files!.isEmpty) return;

    final file = input.files![0];
    final reader = html.FileReader();

    reader.readAsArrayBuffer(file);
    await reader.onLoadEnd.first;

    if (reader.readyState != html.FileReader.DONE) return;

    try {
      final Uint8List bytes = reader.result as Uint8List;
      String text = String.fromCharCodes(bytes);

      setState(() {
        _controller.text = text;
        _processInput(text);
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            "File '${file.name}' uploaded and encoded successfully!",
          ),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Error reading file: $e")));
    }
  }

  Future<void> _downloadEncoded() async {
    if (_encodedResult.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("No encoded data to download.")),
      );
      return;
    }
    if (!kIsWeb) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("File download is only implemented for Web."),
        ),
      );
      return;
    }

    String codeTableString = _huffman.codeTable.entries
        .map(
          (e) =>
              "${e.key.replaceAll('\n', '\\n').replaceAll('\r', '\\r')}:${e.value}",
        )
        .join('|');

    String fileContent =
        "CODES_START:$codeTableString\n\nENCODED_DATA_START:$_encodedResult";

    final bytes = Uint8List.fromList(fileContent.codeUnits);
    final blob = html.Blob([bytes]);
    final url = html.Url.createObjectUrlFromBlob(blob);

    final anchor = html.AnchorElement(href: url)
      ..setAttribute("download", "huffman_encoded.txt")
      ..click();

    html.Url.revokeObjectUrl(url);

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text("Encoded file download triggered!")),
    );
  }

  void _buildGraphDisplay() {
    _graph.nodes.clear();
    _graph.edges.clear();

    if (_huffman.root == null) return;

    void traverse(HuffmanNode node) {
      if (!_graph.nodes.any((n) => n.key?.value == node)) {
        _graph.addNode(Node.Id(node));
      }

      if (node.left != null) {
        _graph.addEdge(Node.Id(node), Node.Id(node.left!));
        traverse(node.left!);
      }
      if (node.right != null) {
        _graph.addEdge(Node.Id(node), Node.Id(node.right!));
        traverse(node.right!);
      }
    }

    traverse(_huffman.root!);
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text("Huffman Coding Algorithm & Entropy"),
          bottom: const TabBar(
            tabs: [
              Tab(icon: Icon(Icons.compare_arrows), text: "Converter"),
              Tab(icon: Icon(Icons.account_tree), text: "Tree Visualizer"),
            ],
          ),
        ),
        body: TabBarView(
          physics: const NeverScrollableScrollPhysics(),
          children: [_buildConverterTab(), _buildVisualizerTab()],
        ),
      ),
    );
  }

  Widget _buildConverterTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              ElevatedButton.icon(
                onPressed: _uploadAndEncode,
                icon: const Icon(Icons.upload_file),
                label: const Text("Upload & Encode (Web)"),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.teal,
                  foregroundColor: Colors.white,
                ),
              ),
              ElevatedButton.icon(
                onPressed: _downloadEncoded,
                icon: const Icon(Icons.download),
                label: const Text("Download Encoded (Web)"),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.indigo,
                  foregroundColor: Colors.white,
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),

          TextField(
            controller: _controller,
            decoration: const InputDecoration(
              labelText: "1. Enter text to encode (e.g., 'Algorithms')",
              border: OutlineInputBorder(),
              suffixIcon: Icon(Icons.keyboard),
            ),
            onChanged: _processInput,
          ),
          const SizedBox(height: 20),

          if (_controller.text.isNotEmpty) ...[
            Card(
              color: Colors.blue.shade50,
              elevation: 2,
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        _statItem(
                          "Original Bits",
                          "${_controller.text.length * 8}",
                          color: Colors.black,
                        ),
                        _statItem(
                          "Total Bits",
                          "${_encodedResult.length}",
                          color: Colors.black,
                        ),
                        _statItem(
                          "Compression %",
                          _controller.text.isEmpty
                              ? "0%"
                              : "${(100 - (_encodedResult.length / (_controller.text.length * 8) * 100)).toStringAsFixed(1)}%",
                          color: Colors.red,
                        ),
                      ],
                    ),
                    const Divider(height: 25, thickness: 1),

                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        _statItem(
                          "Shannon Entropy (H)",
                          "${_shannonEntropy.toStringAsFixed(3)} bits/symbol",
                          color: Colors.black54,
                        ),
                        _statItem(
                          "Avg. Huffman Length (L̄)",
                          "${_averageCodeLength.toStringAsFixed(3)} bits/symbol",
                          color: Colors.blue,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),

            const Text(
              "2. Encoded Binary Output:",
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            Container(
              margin: const EdgeInsets.only(top: 8),
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.grey.shade200,
                borderRadius: BorderRadius.circular(8),
              ),
              child: SelectableText(
                _encodedResult,
                style: const TextStyle(
                  fontFamily: 'monospace',
                  letterSpacing: 1.5,
                ),
              ),
            ),
            const SizedBox(height: 30),

            const Text(
              "3. Decode Binary Sequence:",
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            ),
            const SizedBox(height: 10),

            TextField(
              controller: _encodedController,
              decoration: InputDecoration(
                labelText: "Enter binary sequence (or use auto-filled)",
                border: const OutlineInputBorder(),
                suffixIcon: IconButton(
                  icon: const Icon(Icons.clear),
                  onPressed: () {
                    _encodedController.clear();
                    _decodeInput("");
                  },
                ),
              ),
              onChanged: _decodeInput,
            ),
            const SizedBox(height: 15),

            const Text(
              "4. Decoded Text Output:",
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            Container(
              margin: const EdgeInsets.only(top: 8),
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.lightGreen.shade50,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.green, width: 1),
              ),
              child: SelectableText(
                _decodedResult.isEmpty && _encodedController.text.isNotEmpty
                    ? "Decoding failed (Invalid sequence or missing characters in the lookup table)."
                    : _decodedResult,
                style: TextStyle(
                  fontFamily: 'monospace',
                  letterSpacing: 0.5,
                  color:
                      _decodedResult.isEmpty &&
                          _encodedController.text.isNotEmpty
                      ? Colors.red
                      : Colors.black,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ),
            const SizedBox(height: 20),

            const Text(
              "Lookup Table (Huffman Codes):",
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8.0,
              runSpacing: 8.0,
              children: _huffman.codeTable.entries.map((e) {
                return Chip(
                  avatar: CircleAvatar(
                    backgroundColor: Colors.blue.shade900,
                    child: Text(
                      e.key,
                      style: const TextStyle(color: Colors.white, fontSize: 10),
                    ),
                  ),
                  label: Text(
                    e.value,
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  backgroundColor: Colors.blue.shade100,
                );
              }).toList(),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildVisualizerTab() {
    if (_huffman.root == null) {
      return const Center(
        child: Text(
          "Enter text in Converter tab first to build the Huffman Tree.",
        ),
      );
    }

    return InteractiveViewer(
      constrained: false,
      boundaryMargin: const EdgeInsets.all(50),
      minScale: 0.01,
      maxScale: 5.6,
      child: GraphView(
        graph: _graph,
        algorithm: BuchheimWalkerAlgorithm(
          _builder,
          TreeEdgeRenderer(_builder),
        ),
        paint: Paint()
          ..color = Colors.grey
          ..strokeWidth = 1.5
          ..style = PaintingStyle.stroke,
        builder: (Node node) {
          var hNode = node.key?.value as HuffmanNode;
          bool isLeaf = hNode.isLeaf;
          String code = _huffman.codeTable[hNode.character] ?? '';

          return Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: isLeaf ? Colors.green.shade100 : Colors.orange.shade100,
              border: Border.all(
                color: isLeaf ? Colors.green : Colors.orange,
                width: 2,
              ),
            ),
            child: Text(
              isLeaf
                  ? "'${hNode.character}'\n(${hNode.frequency})\n$code"
                  : "${hNode.frequency}",
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
            ),
          );
        },
      ),
    );
  }

  Widget _statItem(String label, String value, {Color color = Colors.blue}) {
    return Column(
      children: [
        Text(
          value,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
        Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey)),
      ],
    );
  }
}
