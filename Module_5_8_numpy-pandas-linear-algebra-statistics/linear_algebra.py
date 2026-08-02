# Create two vectors v1 = [2, 4, 6] and v2 = [1, 3, 5]. Compute their dot product, the norm of each,
# and the angle between them (hint: cos θ = v1·v2 / (||v1|| × ||v2||)). Then create a 3×3 matrix,
# compute its transpose and inverse.

import numpy as np

v1 = np.array([2, 4, 6])
v2 = np.array([1, 3, 5])

dot_product = np.dot(v1, v2)
v1_norm = np.linalg.norm(v1)
v2_norm = np.linalg.norm(v2)
cos_theta = dot_product / (v1_norm * v2_norm)
angle = np.degrees(np.arccos(cos_theta))
print(f"Dot product: {dot_product}")
print(f"v1 norm: {v1_norm}")
print(f"v2 norm: {v2_norm}")
print(f"Angle between vectors: {angle: .2f} deg")

# 3x3 matrix
A = np.array([[1, 6, 4],
              [5, 9, 2],
              [3, 8, 6]])

# Transpose
print(f"Transpse: {A.T}")

# Inverse
print(f"Inverse{np.linalg.inv(A)}")
