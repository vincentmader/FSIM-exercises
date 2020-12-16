import numpy as np
import matplotlib.pyplot as plt


# Reads a square image in 8-bit/color PPM format from the given file.
# Note: No checks on valid format are done.
def readImage(filename):
    with open(filename, "rb") as f:
        f.readline()
        s = f.readline()
        f.readline()
        (pixel, pixel) = [t(s) for t, s in zip((int, int), s.split())]

        data = np.fromfile(f, dtype=np.uint8, count=pixel*pixel*3)
        img = data.reshape((pixel, pixel, 3)).astype(np.double)

    return img, pixel


# Writes a square image in 8-bit/color PPM format.
def writeImage(filename, image):
    with open(filename, "w") as f:
        pixel = image.shape[0]
        f.writelines("P6\n%d %d\n%d\n" % (pixel, pixel, 255))

        image = image.astype(np.uint8)

        image.tofile(f)


def print_color_sums(img):
    r_sum, g_sum, b_sum, total_sum = 0, 0, 0, 0
    for row in img:
        for px in row:
            r, g, b = px[0], px[1], px[2]
            r_sum += r
            g_sum += g
            b_sum += b
            total_sum += r + g + b
    print('r:', int(r_sum))
    print('g:', int(g_sum))
    print('b:', int(b_sum))
    print('total:', int(total_sum))


img, pixel = readImage("../figures/aq-original.ppm")

print_color_sums(img)


# Now we set up our desired smoothing kernel.
# We'll use complex number for it even though it is real.
kernel_real = np.zeros((pixel, pixel), dtype=np.complex)
# set smoothing length
hsml = 10.

# now set the values of the kernel
for i in np.arange(pixel):
    for j in np.arange(pixel):
        # TODO: do something sensible here to set the real part of the kernel
        r = np.sqrt(i**2 + j**2)
        x = r / hsml
        if 0 <= x < .5:
            kernel_value = 1 - 6*x**2 + 6*x**3
        elif .5 <= x < 1:
            kernel_value = 2 * (1 - x)**3
        else:
            kernel_value = 0

        kernel_real[i][j] = kernel_value


# Let's calculate the Fourier transform of the kernel
kernel_kspace = np.fft.fft2(kernel_real)

# further space allocations for image transforms
color_real = np.zeros((pixel, pixel), dtype=np.complex)

# we now convolve each color channel with the kernel using FFTs
for colindex in np.arange(3):
    # copy input color into complex array
    color_real[:, :].real = img[:, :, colindex]

    # forward transform
    color_kspace = np.fft.fft2(color_real)

    # multiply with kernel in Fourier space
    # TODO: fill in code here
    color_kspace *= kernel_real

    # backward transform
    color_real = np.fft.ifft2(color_kspace)

    # copy real value of complex result back into color array
    img[:, :, colindex] = color_real.real

print_color_sums(img)

writeImage("../figures/aq-smoothed.ppm", img)
