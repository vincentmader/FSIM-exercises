import matplotlib.pyplot as plt

from get_list_of_N_float_tuples import main as get_list_of_N_float_tuples


def main():
    list_of_random_float_tuples = get_list_of_N_float_tuples(1000)

    x = [i[0] for i in list_of_random_float_tuples]
    y = [i[1] for i in list_of_random_float_tuples]

    plt.figure(figsize=(4, 4))
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.scatter(x, y, color='red', s=3)
    plt.savefig('fig1.pdf')
    plt.close()


if __name__ == "__main__":
    main()
