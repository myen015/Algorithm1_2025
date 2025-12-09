# Problem Set #7 — Fundamental Algorithm Techniques  
**Review on November 22**

---

## **Problem 1 — Graph Play (3 pts)**

Below are my examples and answers for all five sub-questions about directed, undirected, inverse, and dual graphs.

---

### **1. Examples of directed graphs and their transposed versions**

Consider the directed graph:

- A → B  
- A → C  
- C → B  
- B → D  

**Transposed graph:**  
Every edge is reversed:

- B → A  
- C → A  
- B → C  
- D → B  

---

### **2. Examples of undirected graphs and their inverse graphs**

Example undirected graph:

- A — B  
- A — C  
- B — C  
- C — D  

Non-edges: (A,D) and (B,D)

**Inverse graph:**  
Edges become:

- A — D  
- B — D  

All edges present in the original graph disappear.

---

### **3. What if the original graph is dense?**

If the original graph is very dense (close to a complete graph), then:

- its inverse graph becomes very sparse  
- very few pairs remain “non-edges” to turn into inverse edges  

In the extreme case (complete graph), the inverse graph has **zero edges**.

---

### **4. Simple examples of undirected graphs and their duals**

Dual graphs are defined only for planar graphs.

**Example 1:** A triangle ABC  
- It has only one face  
- The dual graph contains a single vertex

**Example 2:** A square with a diagonal  
- The diagonal splits the square into two triangular faces  
- Dual graph has 2 vertices connected by an edge

---

### **5. Why is the dual defined only for planar graphs? Example of a non-planar graph**

The dual graph is constructed by:

1. Taking a planar embedding  
2. Placing one node inside each face  
3. Connecting nodes whose faces share an edge  

If a graph is *not planar*, then **no planar embedding exists**, and therefore “faces” are not defined → the dual cannot be constructed.

**Example of a non-planar graph without a dual:**  
- **K₃,₃** (classic non-planar graph)

---

# **Problem 2 — Bron–Kerbosch Algorithm (7 pts)**

We are given the undirected graph:

- V = {A, B, C, D}  
- E = {AB, AC, BC, CD}

Adjacency list:

```python
graph = {
    "A": ["B", "C"],
    "B": ["A", "C"],
    "C": ["A", "B", "D"],
    "D": ["C"]
}
