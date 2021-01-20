from get_list_of_N_random_ints import main as get_list_of_N_random_ints
from normalize import main as normalize


def main(N):
    list_of_random_float_tuples = []
    list_of_random_ints = get_list_of_N_random_ints(N + 1)

    for idx, item in enumerate(list_of_random_ints[:-1]):
        a, b = item, list_of_random_ints[idx + 1]

        list_of_random_float_tuples.append(
            (normalize(a), normalize(b))
        )

    return list_of_random_float_tuples
