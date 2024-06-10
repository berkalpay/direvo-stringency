import itertools
import numpy as np
from sampling import compute_results, update_saved_results


def sample_max(n_low: int, alpha: float, n_sum: int, delta_x: float = 1) -> float:
    dfe_param = np.random.exponential(1 / alpha, 2)
    x_low = np.random.exponential(1 / dfe_param[0], n_low) - delta_x
    x_high = np.random.exponential(1 / dfe_param[1], n_sum - n_low)
    return np.log(max(itertools.chain(x_low, x_high)))


def make_param_grid(alphas: tuple, n_sums: tuple) -> list[tuple]:
    grid = []
    for alpha, n_sum in itertools.product(alphas, n_sums):
        for n_low in range(0, n_sum):
            grid.append((n_low, alpha, n_sum))
    return grid


if __name__ == "__main__":
    param_grid = make_param_grid(alphas=(0.01, 0.1, 10), n_sums=(10, 100, 1000))
    results = compute_results(sample_max, param_grid, 10**5)
    update_saved_results(
        results,
        "results/sampling_two_dfes.csv",
        parameter_names=["n_low", "alpha", "n"],
    )
