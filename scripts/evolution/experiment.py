import os
import itertools
import random
from multiprocessing import Pool
import numpy as np
from evolution import Variant, Landscape, standard_landscape, DirectedEvolution

n_gen = 20
pop_size = 100
ks = list(range(1, 11)) + [15, 20, 30, 40, 50, 75, 100]
recover_ps = [0]
delta_magnitudes = [0.2, 0.5, 1]
delta_ps = [0.1, 0.5, 0.8]


def run_selection_experiment(
    wildtype: Variant,
    pop_size: int,
    landscape: Landscape,
    n_to_select: int,
    n_gen: int,
    seed: int = None,
    mutagenesis_sampling="multinomial",
) -> DirectedEvolution:
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    initial_pop = [wildtype] * pop_size
    de = DirectedEvolution(initial_pop, landscape)
    de.run(n_to_select, n_gen, mutagenesis_sampling)
    return de


if __name__ == "__main__":
    n_sims = 2000
    n_parallel_sims = 50

    for _ in range(n_sims // n_parallel_sims):
        for delta_magnitude, delta_p, recover_p, k in itertools.product(
            delta_magnitudes, delta_ps, recover_ps, ks
        ):
            # Run experiments
            seeds = [random.randint(0, 2**32 - 1) for _ in range(n_parallel_sims)]
            params = [
                (
                    Variant(0, 1),
                    pop_size,
                    standard_landscape(delta_magnitude, delta_p, recover_p),
                    k,
                    n_gen,
                    seed,
                )
                for seed in seeds
            ]
            with Pool() as pool:
                des = pool.starmap(run_selection_experiment, params)

            # Write results
            results_fn = "results/evo_experiment.csv"
            results_exist = os.path.exists(results_fn)
            with open(results_fn, "a") as f:
                if not results_exist:
                    attr_names = ["seed", "n", "k", "gen",
                                  "delta_magnitude", "delta_p", "recover_p",
                                  "max_fitness"]  # fmt: skip
                    f.write(",".join(attr_names) + "\n")
                for de, seed in zip(des, seeds):
                    for gen in range(len(de)):
                        attrs = [seed, pop_size, k, gen,
                                 delta_magnitude, delta_p, recover_p,
                                 de.max_fitness(gen)]  # fmt: skip
                        f.write(",".join(map(str, attrs)) + "\n")
