function matrixMultiply(a, b) {
  const result = [
    [0, 0],
    [0, 0],
  ];

  result[0][0] = a[0][0] * b[0][0] + a[0][1] * b[1][0];
  result[0][1] = a[0][0] * b[0][1] + a[0][1] * b[1][1];
  result[1][0] = a[1][0] * b[0][0] + a[1][1] * b[1][0];
  result[1][1] = a[1][0] * b[0][1] + a[1][1] * b[1][1];

  return result;
}

function matrixPower(matrix, n) {
  if (n === 0) {
    return [
      [1, 0],
      [0, 1],
    ];
  }

  if (n === 1) {
    return matrix;
  }

  if (n % 2 === 0) {
    const half = matrixPower(matrix, n / 2);
    return matrixMultiply(half, half);
  } else {
    const half = matrixPower(matrix, Math.floor(n / 2));
    return matrixMultiply(matrixMultiply(half, half), matrix);
  }
}

function fastFibonacci_n(n) {
  if (n < 0) {
    return null;
  }

  if (n === 0) {
    return 0;
  }
  if (n === 1) {
    return 1;
  }

  const transformationMatrix = [
    [1, 1],
    [1, 0],
  ];

  const poweredMatrix = matrixPower(transformationMatrix, n);

  const F_n = poweredMatrix[1][0];

  return F_n;
}

//implementation of fastFibonacci_half_n is excluded

const n = 5;
console.log(`F(${n}) =`, fastFibonacci_n(n));

//https://www.geeksforgeeks.org/dsa/matrix-exponentiation/
