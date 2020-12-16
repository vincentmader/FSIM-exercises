from numpy import uint64, power


def main(previous_int):
    # make sure all variables are 64-bit floats
    previous_int = uint64(previous_int)
    a = uint64(65539)
    b = uint64(2)
    c = uint64(31)

    return (a * previous_int) % power(b, c)
