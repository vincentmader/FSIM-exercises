#include <stdio.h>
#include <stdbool.h>


long double find_epsilon () {

    long double one = 1;
    long double epsilon = 1;
    long double new_epsilon;

    bool found_epsilon = false;
    while (!found_epsilon) {
        new_epsilon = epsilon / 2.;
        if (one + new_epsilon == one) {
            return epsilon;
        }
        epsilon = new_epsilon;
    }
}

int main(void) {
    printf(
        "%e \n", find_epsilon()
    );
}
