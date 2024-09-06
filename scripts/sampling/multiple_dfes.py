import itertools
import numpy as np
from sampling import log_seq, compute_results, update_saved_results


def allocate(n: int, k: int):
    remaining = np.array([0] * (k - (n % k)) + [1] * (n % k))
    np.random.shuffle(remaining)
    return np.repeat(int(n / k), k) + remaining


def sample_max(k: int, alpha: float, n_sum: int, delta: int = 1) -> float:
    n = allocate(n_sum, k)
    dfe_param = np.random.exponential(1 / alpha, k)
    x_by_parent = [np.random.exponential(1 / dfe_param[0], n[0])]
    for i in range(1, k):
        x_by_parent.append(np.random.exponential(1 / dfe_param[i], n[i]) - delta)
    return np.log(max(itertools.chain(*x_by_parent)))


def sample_max_alt1(k: int, alpha: float, n_sum: int, delta: int = 1) -> float:
    n = allocate(n_sum, k)
    dfe_param = np.sqrt(np.random.exponential(alpha, k))
    x_by_parent = [np.random.normal(dfe_param[0], 1, n[0])]
    for i in range(1, k):
        x_by_parent.append(np.random.normal(dfe_param[i], 1, n[i]) - delta)
    return max(itertools.chain(*x_by_parent))


def sample_max_alt2(k: int, alpha: float, n_sum: int, delta: int = 1) -> float:
    n = allocate(n_sum, k)
    dfe_param = np.sqrt(np.random.exponential(alpha, k))
    x_by_parent = [np.random.normal(0, dfe_param[0], n[0])]
    for i in range(1, k):
        x_by_parent.append(np.random.normal(0, dfe_param[i], n[i]) - delta)
    return max(itertools.chain(*x_by_parent))


def make_param_grid(alphas: tuple, n_sums: tuple, max_num_ks: int = 100) -> list[tuple]:
    grid = []
    for alpha, n_sum in itertools.product(alphas, n_sums):
        for k in log_seq(n_sum, max_num_ks):
            grid.append((k, alpha, n_sum))
    return grid


parameter_names = ["k", "alpha", "n"]


if __name__ == "__main__":
    param_grid = make_param_grid(alphas=(0.001, 0.01, 1), n_sums=(10, 100, 1000))
    results = compute_results(sample_max, param_grid, 10**5)
    update_saved_results(results, "results/sampling_multiple_dfes.csv", parameter_names)

    param_grid = make_param_grid(alphas=(0.1, 5, 100), n_sums=(10, 100, 1000))
    results = compute_results(sample_max_alt1, param_grid, 10**5)
    update_saved_results(
        results, "results/sampling_multiple_dfes_alt1.csv", parameter_names
    )

    results = compute_results(sample_max_alt2, param_grid, 10**5)
    update_saved_results(
        results, "results/sampling_multiple_dfes_alt2.csv", parameter_names
    )
