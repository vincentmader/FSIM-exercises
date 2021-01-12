import numpy as np


n = 100
grid_3D = np.zeros(shape=(n, n, n))


def convert_3D_grid_to_1D_vector(grid, n):

    vector = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                grid_cell = grid[i][j][k]
                vector.append(grid_cell)

    return vector


def convert_1D_vector_to_3D_grid(vector, n):

    grid = np.zeros(shape=(n, n, n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                grid_cell = vector[i*n**2 + j*n + k]
                grid[i][j][k] = grid_cell

    return grid


grid = np.random.rand(n, n, n)
vector = convert_3D_grid_to_1D_vector(grid, n)
new_grid = convert_1D_vector_to_3D_grid(vector, n)

print((new_grid == grid).all())
