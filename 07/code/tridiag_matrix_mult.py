def main(a, b, c, v):

    n = len(a)
    out = np.zeros(shape=(n, n))

    # first row of matrix
    out[0][0] = a[0] * v[0]
    out[0][1] = b[0] * v[1]

    # second to second-last rows
    for i in range(1, n-1):
        for j in range(1, n-1):
            if i == j:
                out[i][j] = a[i] * v[i]
            elif i == j-1:
                out[i][j] = b[i] * v[j]
            elif i == j+1:
                out[i][j] = c[i] * v[j]

    # last row
    out[-1][-2] = c[-2] * v[-2]
    out[-1][-1] = a[-1] * v[-1]

    return out
