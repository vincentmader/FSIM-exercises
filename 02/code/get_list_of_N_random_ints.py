from numpy import uint64

from get_next_RANDU_int import main as get_next_RANDU_int


def main(N):
    list_of_random_ints = [uint64(1)]

    for _ in range(N):
        i = list_of_random_ints[-1]
        j = get_next_RANDU_int(i)
        list_of_random_ints.append(j)

    return list_of_random_ints


if __name__ == '__main__':
    first_1000_ints = main(1000)
