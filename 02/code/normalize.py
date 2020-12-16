from numpy import uint64, power


def main(num):
    return num / power(uint64(2), uint64(31))
