# Transportation Problem Solver

This project solves the **Transportation Problem** (minimizing logistics costs) using three distinct algorithms, ranging from basic heuristics to mathematical optimization. It visualizes the supply chain network and calculates the cost savings achieved through optimization.

## Project Overview

The goal is to determine the optimal way to transport goods from multiple suppliers (Sources) to multiple consumers (Destinations) while minimizing total shipping costs. The code demonstrates the difference between a naive initial guess and a mathematically optimized solution.

### Algorithms Implemented

#### 1. Northwest Corner Method (Basic Feasible Solution)
This is a naive heuristic used to establish a starting point.
* **Logic:** It starts at the top-left cell (0,0) and allocates as much as possible without considering shipping costs. It moves right if the supply is exhausted, or down if the demand is satisfied.
* **Result:** Provides a valid but usually expensive and inefficient plan. It serves as a baseline to measure optimization improvements.

#### 2. Russell's Approximation Method (Advanced Heuristic)
A more intelligent method for finding an initial feasible solution that considers costs.
* **Logic:** For every row and column, it identifies the largest shipping cost ($U_i$ and $V_j$). It then calculates an opportunity cost $\Delta_{ij}$ for every cell:
    $$\Delta_{ij} = C_{ij} - (U_i + V_j)$$
    Allocations are prioritized for cells with the most negative $\Delta_{ij}$ values.
* **Result:** A "near-optimal" solution that is significantly cheaper than the Northwest Corner method.

#### 3. Simplex Method (MODI / Stepping Stone)
An iterative optimization algorithm that guarantees the mathematically minimal cost.
* **Logic:**
    1.  **Potentials:** Calculates dual variables ($u_i, v_j$) for all rows and columns such that $u_i + v_j = C_{ij}$ for occupied cells.
    2.  **Optimality Test:** Checks unoccupied cells for improvement potential using the reduced cost formula: $\text{Improvement}_{ij} = C_{ij} - (u_i + v_j)$. If this value is negative, shifting goods here will lower the total cost.
    3.  **Looping:** If a better path is found, it traces a closed cycle (stepping stone path) through existing allocations to shift flow into the new cell while maintaining supply/demand balance.
* **Result:** The absolute minimum possible cost.

## Code Structure

* **Logic:** Custom Python implementations of the algorithms mentioned above without relying on external solvers for the core logic.
* **Visualization:** Uses `NetworkX` and `Matplotlib` to draw a directed graph connecting suppliers to consumers. The edge thickness represents the volume of goods.
* **Validation:** Includes a comparison module that runs the same data through `SciPy` and `PuLP` libraries to verify that the custom Simplex implementation is correct.
