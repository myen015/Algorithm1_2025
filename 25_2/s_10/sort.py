import numpy as np
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

# ============================================================================
# FUNCTIONAL LINK NEURAL NETWORK (FLNN) IMPLEMENTATION
# ============================================================================

class FLNN:
    """
    A simple 3-layer Functional Link Neural Network
    Architecture: Input -> Functional Expansion -> Hidden -> Output
    """
    
    def __init__(self, input_size=4, hidden_size=4, output_size=1, learning_rate=0.1):
        """
        Initialize the FLNN with random weights
        
        Parameters:
        - input_size: number of input features (4 in our case)
        - hidden_size: number of hidden neurons (4 in our case)
        - output_size: number of output neurons (1 in our case)
        - learning_rate: step size for weight updates
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        
        # Initialize weights randomly (small values)
        # V: weights from functional expansion to hidden layer (4x5 including bias)
        self.V = np.random.randn(hidden_size, input_size + 1) * 0.5
        
        # W: weights from hidden layer to output (1x5 including bias)
        self.W = np.random.randn(output_size, hidden_size + 1) * 0.5
        
        # Store errors for plotting
        self.errors = []
        
    def functional_expansion(self, X):
        """
        Apply functional expansion: phi(x) = sin(x)
        This is the key feature of FLNN!
        
        Parameters:
        - X: input data (can be single sample or batch)
        
        Returns:
        - phi: transformed input with bias term added
        """
        # Apply sin transformation to each input
        phi = np.sin(X)
        
        # Add bias term (column of ones)
        if phi.ndim == 1:
            # Single sample
            phi = np.append(phi, 1)
        else:
            # Multiple samples
            bias = np.ones((phi.shape[0], 1))
            phi = np.hstack([phi, bias])
        
        return phi
    
    def sigmoid(self, x):
        """
        Sigmoid activation function: 1 / (1 + e^(-x))
        """
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))  # clip to avoid overflow
    
    def sigmoid_derivative(self, x):
        """
        Derivative of sigmoid: sigmoid(x) * (1 - sigmoid(x))
        """
        s = self.sigmoid(x)
        return s * (1 - s)
    
    def forward(self, X):
        """
        Forward propagation through the network
        
        Steps:
        1. Apply functional expansion: phi = sin(X)
        2. Compute hidden layer: h = sigmoid(V * phi)
        3. Compute output: o = sigmoid(W * h)
        
        Parameters:
        - X: input data
        
        Returns:
        - output: network prediction
        """
        # Step 1: Functional expansion
        self.phi = self.functional_expansion(X)
        
        # Step 2: Hidden layer computation
        # net_h = V * phi (matrix multiplication)
        self.net_hidden = np.dot(self.V, self.phi)
        # Apply sigmoid activation
        self.hidden = self.sigmoid(self.net_hidden)
        
        # Add bias to hidden layer output
        self.hidden_with_bias = np.append(self.hidden, 1)
        
        # Step 3: Output layer computation
        # net_o = W * h
        self.net_output = np.dot(self.W, self.hidden_with_bias)
        # Apply sigmoid activation
        self.output = self.sigmoid(self.net_output)
        
        return self.output
    
    def backward(self, X, y):
        """
        Backward propagation (backpropagation)
        
        Steps:
        1. Compute output error: delta_o = -(t - o) * o * (1 - o)
        2. Update output weights: W = W - eta * delta_o * h
        3. Compute hidden error: delta_h = delta_o * W * h * (1 - h)
        4. Update hidden weights: V = V - eta * delta_h * phi
        
        Parameters:
        - X: input data
        - y: target output
        """
        # Number of samples
        m = 1  # we're doing stochastic (one sample at a time)
        
        # Step 1: Calculate output layer error signal
        # delta_o = -(target - output) * sigmoid_derivative(net_output)
        output_error = -(y - self.output)
        delta_output = output_error * self.sigmoid_derivative(self.net_output)
        
        # Step 2: Update output layer weights
        # dW = delta_o * h^T
        dW = np.outer(delta_output, self.hidden_with_bias)
        self.W -= self.learning_rate * dW
        
        # Step 3: Calculate hidden layer error signal
        # Remove bias weight from W for backprop
        W_no_bias = self.W[:, :-1]  # exclude bias weight
        
        # delta_h = W^T * delta_o * sigmoid_derivative(net_hidden)
        delta_hidden = np.dot(W_no_bias.T, delta_output) * self.sigmoid_derivative(self.net_hidden)
        
        # Step 4: Update hidden layer weights
        # dV = delta_h * phi^T
        dV = np.outer(delta_hidden, self.phi)
        self.V -= self.learning_rate * dV
    
    def train(self, X, y, epochs=1000, patience=50, min_delta=1e-6):
        """
        Train the network using stochastic gradient descent with early stopping
        
        Parameters:
        - X: training inputs (n_samples x n_features)
        - y: training targets (n_samples x 1)
        - epochs: maximum number of training iterations
        - patience: number of epochs to wait for improvement before stopping
        - min_delta: minimum change in loss to be considered as improvement
        """
        n_samples = X.shape[0]
        
        print("Starting training...")
        print(f"Dataset size: {n_samples} samples")
        print(f"Max epochs: {epochs}")
        print(f"Learning rate: {self.learning_rate}")
        print(f"Early stopping: patience={patience}, min_delta={min_delta}")
        print("-" * 50)
        
        best_loss = float('inf')
        patience_counter = 0
        
        for epoch in range(epochs):
            epoch_error = 0
            
            # Train on each sample (stochastic learning)
            for i in range(n_samples):
                # Get single sample
                x_sample = X[i]
                y_sample = y[i]
                
                # Forward pass
                output = self.forward(x_sample)
                
                # Calculate error for this sample
                error = 0.5 * (y_sample - output) ** 2
                epoch_error += error
                
                # Backward pass (update weights)
                self.backward(x_sample, y_sample)
            
            # Calculate mean squared error for this epoch
            mse = epoch_error / n_samples
            self.errors.append(mse[0])
            
            # Early stopping check
            if mse[0] < best_loss - min_delta:
                best_loss = mse[0]
                patience_counter = 0
            else:
                patience_counter += 1
            
            # Print progress every 100 epochs
            if (epoch + 1) % 100 == 0:
                print(f"Epoch {epoch + 1}/{epochs} - MSE: {mse[0]:.6f}")
            
            # Stop if no improvement for 'patience' epochs
            if patience_counter >= patience:
                print(f"\nEarly stopping at epoch {epoch + 1}")
                print(f"No improvement for {patience} consecutive epochs")
                print(f"Best MSE: {best_loss:.6f}")
                break
        
        print("-" * 50)
        print("Training completed!")
        return epoch + 1  # Return actual number of epochs
    
    def predict(self, X):
        """
        Make predictions on new data
        
        Parameters:
        - X: input data
        
        Returns:
        - predictions
        """
        if X.ndim == 1:
            # Single sample
            return self.forward(X)
        else:
            # Multiple samples
            predictions = []
            for x in X:
                pred = self.forward(x)
                predictions.append(pred)
            return np.array(predictions)


# ============================================================================
# STANDARD FEEDFORWARD NEURAL NETWORK (FFNN) IMPLEMENTATION
# ============================================================================

class StandardFFNN:
    """
    Standard 3-layer Feedforward Neural Network (WITHOUT functional expansion)
    Architecture: Input -> Hidden -> Output
    """
    
    def __init__(self, input_size=4, hidden_size=4, output_size=1, learning_rate=0.1):
        """
        Initialize the Standard FFNN with random weights
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        
        # Initialize weights randomly (small values)
        # V: weights from input to hidden layer (4x5 including bias)
        self.V = np.random.randn(hidden_size, input_size + 1) * 0.5
        
        # W: weights from hidden layer to output (1x5 including bias)
        self.W = np.random.randn(output_size, hidden_size + 1) * 0.5
        
        # Store errors for plotting
        self.errors = []
    
    def add_bias(self, X):
        """Add bias term to input"""
        if X.ndim == 1:
            return np.append(X, 1)
        else:
            bias = np.ones((X.shape[0], 1))
            return np.hstack([X, bias])
    
    def sigmoid(self, x):
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def sigmoid_derivative(self, x):
        """Derivative of sigmoid"""
        s = self.sigmoid(x)
        return s * (1 - s)
    
    def forward(self, X):
        """
        Forward propagation through standard FFNN
        NO functional expansion - direct input
        """
        # Add bias to input (NO sin transformation)
        self.input_with_bias = self.add_bias(X)
        
        # Hidden layer computation
        self.net_hidden = np.dot(self.V, self.input_with_bias)
        self.hidden = self.sigmoid(self.net_hidden)
        
        # Add bias to hidden layer output
        self.hidden_with_bias = np.append(self.hidden, 1)
        
        # Output layer computation
        self.net_output = np.dot(self.W, self.hidden_with_bias)
        self.output = self.sigmoid(self.net_output)
        
        return self.output
    
    def backward(self, X, y):
        """Backward propagation for standard FFNN"""
        # Output layer error
        output_error = -(y - self.output)
        delta_output = output_error * self.sigmoid_derivative(self.net_output)
        
        # Update output weights
        dW = np.outer(delta_output, self.hidden_with_bias)
        self.W -= self.learning_rate * dW
        
        # Hidden layer error
        W_no_bias = self.W[:, :-1]
        delta_hidden = np.dot(W_no_bias.T, delta_output) * self.sigmoid_derivative(self.net_hidden)
        
        # Update hidden weights
        dV = np.outer(delta_hidden, self.input_with_bias)
        self.V -= self.learning_rate * dV
    
    def train(self, X, y, epochs=1000, patience=50, min_delta=1e-6):
        """Train the standard FFNN with early stopping"""
        n_samples = X.shape[0]
        
        print("Starting training...")
        print(f"Dataset size: {n_samples} samples")
        print(f"Max epochs: {epochs}")
        print(f"Learning rate: {self.learning_rate}")
        print(f"Early stopping: patience={patience}, min_delta={min_delta}")
        print("-" * 50)
        
        best_loss = float('inf')
        patience_counter = 0
        
        for epoch in range(epochs):
            epoch_error = 0
            
            for i in range(n_samples):
                x_sample = X[i]
                y_sample = y[i]
                
                output = self.forward(x_sample)
                error = 0.5 * (y_sample - output) ** 2
                epoch_error += error
                
                self.backward(x_sample, y_sample)
            
            mse = epoch_error / n_samples
            self.errors.append(mse[0])
            
            # Early stopping check
            if mse[0] < best_loss - min_delta:
                best_loss = mse[0]
                patience_counter = 0
            else:
                patience_counter += 1
            
            if (epoch + 1) % 100 == 0:
                print(f"Epoch {epoch + 1}/{epochs} - MSE: {mse[0]:.6f}")
            
            if patience_counter >= patience:
                print(f"\nEarly stopping at epoch {epoch + 1}")
                print(f"No improvement for {patience} consecutive epochs")
                print(f"Best MSE: {best_loss:.6f}")
                break
        
        print("-" * 50)
        print("Training completed!")
        return epoch + 1
    
    def predict(self, X):
        """Make predictions"""
        if X.ndim == 1:
            return self.forward(X)
        else:
            predictions = []
            for x in X:
                pred = self.forward(x)
                predictions.append(pred)
            return np.array(predictions)


# ============================================================================
# PREPARE DATASET
# ============================================================================

print("\n" + "="*70)
print("FUNCTIONAL LINK NEURAL NETWORK - SEMINAR 4")
print("="*70 + "\n")

# Create a small dataset as specified
# 4 input features, 1 output
X_train = np.array([
    [0.5, 1.0, -0.5, 0.8],
    [-0.3, 0.7, 1.2, -0.4],
    [0.9, -0.6, 0.3, 1.1],
    [-0.8, 0.4, -0.2, 0.5]
])

y_train = np.array([
    [0.6],
    [0.4],
    [0.8],
    [0.3]
])

print("Dataset:")
print("Inputs (X):")
print(X_train)
print("\nTargets (y):")
print(y_train.flatten())
print()


# ============================================================================
# TRAIN FLNN
# ============================================================================

print("\n" + "="*70)
print("TRAINING FLNN (WITH sin(x) FUNCTIONAL EXPANSION)")
print("="*70 + "\n")

# Set same random seed for fair comparison
np.random.seed(42)
flnn = FLNN(input_size=4, hidden_size=4, output_size=1, learning_rate=0.5)

print("Initial Network Weights:")
print("V (input to hidden) shape:", flnn.V.shape)
print("\nW (hidden to output) shape:", flnn.W.shape)
print()

# Train the FLNN
flnn_epochs = flnn.train(X_train, y_train, epochs=2000, patience=100, min_delta=1e-7)


# ============================================================================
# TRAIN STANDARD FFNN
# ============================================================================

print("\n" + "="*70)
print("TRAINING STANDARD FFNN (WITHOUT FUNCTIONAL EXPANSION)")
print("="*70 + "\n")

# Set same random seed for fair comparison
np.random.seed(42)
ffnn = StandardFFNN(input_size=4, hidden_size=4, output_size=1, learning_rate=0.5)

print("Initial Network Weights:")
print("V (input to hidden) shape:", ffnn.V.shape)
print("\nW (hidden to output) shape:", ffnn.W.shape)
print()

# Train the Standard FFNN
ffnn_epochs = ffnn.train(X_train, y_train, epochs=2000, patience=100, min_delta=1e-7)


# ============================================================================
# COMPARE PREDICTIONS
# ============================================================================

print("\n" + "="*70)
print("COMPARISON: FLNN vs STANDARD FFNN")
print("="*70 + "\n")

print("Final Predictions:")
print("-" * 70)
flnn_predictions = flnn.predict(X_train)
ffnn_predictions = ffnn.predict(X_train)

print(f"{'Sample':<8} {'Target':<10} {'FLNN Pred':<12} {'FLNN Error':<12} {'FFNN Pred':<12} {'FFNN Error':<12}")
print("-" * 70)

for i in range(len(X_train)):
    flnn_err = abs(y_train[i][0] - flnn_predictions[i][0])
    ffnn_err = abs(y_train[i][0] - ffnn_predictions[i][0])
    print(f"{i+1:<8} {y_train[i][0]:<10.4f} {flnn_predictions[i][0]:<12.4f} "
          f"{flnn_err:<12.6f} {ffnn_predictions[i][0]:<12.4f} {ffnn_err:<12.6f}")

print()


# ============================================================================
# PLOT COMPARISON: LOSS VS ITERATIONS
# ============================================================================

plt.figure(figsize=(12, 6))

# Plot both networks
plt.plot(flnn.errors, linewidth=2, label='FLNN (with sin(x) expansion)', color='blue')
plt.plot(ffnn.errors, linewidth=2, label='Standard FFNN (no expansion)', color='red', linestyle='--')

plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Mean Squared Error (MSE)', fontsize=12)
plt.title('Training Loss Comparison: FLNN vs Standard FFNN', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.yscale('log')  # Log scale to better see convergence
plt.tight_layout()
plt.savefig('flnn_vs_ffnn_comparison.png', dpi=300, bbox_inches='tight')
print("Comparison plot saved as 'flnn_vs_ffnn_comparison.png'")
plt.show()


# ============================================================================
# DEMONSTRATE FUNCTIONAL EXPANSION
# ============================================================================

print("\n" + "="*70)
print("PART D: ANALYSIS - Impact of Functional Link Expansion")
print("="*70 + "\n")

print("Functional Expansion Example:")
print("-" * 50)
sample_input = X_train[0]
print(f"Original input: {sample_input}")
print(f"After sin() transformation: {np.sin(sample_input)}")
print()

print("Key Benefits of sin(x) Functional Expansion:")
print("1. Introduces non-linearity at the input stage")
print("2. Transforms input space to make patterns more separable")
print("3. Can reduce the need for deep networks")
print("4. Helps capture periodic patterns naturally")
print("5. Often leads to faster convergence")
print()

# Show how different inputs are transformed
print("Transformation visualization:")
x_vals = np.linspace(-2, 2, 50)
phi_vals = np.sin(x_vals)

plt.figure(figsize=(10, 5))
plt.plot(x_vals, x_vals, 'b-', label='Standard FFNN: y = x (identity)', linewidth=2)
plt.plot(x_vals, phi_vals, 'r-', label='FLNN: y = sin(x) (expansion)', linewidth=2)
plt.xlabel('Input value (x)', fontsize=12)
plt.ylabel('Transformed value', fontsize=12)
plt.title('Input Transformation: Identity vs sin(x) Functional Expansion', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig('functional_expansion.png', dpi=300, bbox_inches='tight')
print("Functional expansion plot saved as 'functional_expansion.png'")
plt.show()


# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "="*70)
print("FINAL SUMMARY")
print("="*70)

print("\n--- FLNN (with sin(x) expansion) ---")
print(f"Epochs to converge: {flnn_epochs}")
print(f"Initial MSE:        {flnn.errors[0]:.6f}")
print(f"Final MSE:          {flnn.errors[-1]:.6f}")
print(f"Improvement:        {(1 - flnn.errors[-1]/flnn.errors[0])*100:.2f}%")

print("\n--- Standard FFNN (no expansion) ---")
print(f"Epochs to converge: {ffnn_epochs}")
print(f"Initial MSE:        {ffnn.errors[0]:.6f}")
print(f"Final MSE:          {ffnn.errors[-1]:.6f}")
print(f"Improvement:        {(1 - ffnn.errors[-1]/ffnn.errors[0])*100:.2f}%")

print("\n--- Comparison ---")
epochs_saved = ffnn_epochs - flnn_epochs
if epochs_saved > 0:
    print(f"FLNN converged {epochs_saved} epochs FASTER ({(epochs_saved/ffnn_epochs)*100:.1f}% faster)")
elif epochs_saved < 0:
    print(f"Standard FFNN converged {-epochs_saved} epochs FASTER")
else:
    print("Both networks converged in the same number of epochs")

if flnn.errors[-1] < ffnn.errors[-1]:
    improvement = ((ffnn.errors[-1] - flnn.errors[-1])/ffnn.errors[-1]) * 100
    print(f"FLNN achieved {improvement:.2f}% LOWER final error")
else:
    improvement = ((flnn.errors[-1] - ffnn.errors[-1])/flnn.errors[-1]) * 100
    print(f"Standard FFNN achieved {improvement:.2f}% LOWER final error")

print("\nFLNN Network Architecture:")
print(f"  Input layer:      {flnn.input_size} neurons")
print(f"  Functional layer: sin(x) transformation")
print(f"  Hidden layer:     {flnn.hidden_size} neurons (sigmoid)")
print(f"  Output layer:     {flnn.output_size} neuron (sigmoid)")
print(f"  Total weights:    {flnn.V.size + flnn.W.size}")

print("\nStandard FFNN Architecture:")
print(f"  Input layer:      {ffnn.input_size} neurons (no transformation)")
print(f"  Hidden layer:     {ffnn.hidden_size} neurons (sigmoid)")
print(f"  Output layer:     {ffnn.output_size} neuron (sigmoid)")
print(f"  Total weights:    {ffnn.V.size + ffnn.W.size}")

print("\n" + "="*70)