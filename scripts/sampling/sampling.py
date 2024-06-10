import os
import csv
import random
from itertools import repeat
from collections import UserDict
from typing import NamedTuple, Callable
from multiprocessing import Pool
import numpy as np


def log_seq(n_sum: int, max_len: int) -> set[int]:
    k_fracs = np.linspace(np.log10(1 / n_sum), 0, num=max_len)
    return set(np.rint(10**k_fracs * n_sum).astype(int))


class Result(NamedTuple):
    mean: float
    sample_size: int

    def combine_with(self, other):
        n, m = self.sample_size, other.sample_size
        new_mean = (self.mean * n + other.mean * m) / (n + m)
        return Result(new_mean, int(n + m))


class Results(UserDict):
    def update_with(self, other) -> None:
        for params, new_results in other.data.items():
            if params in self.data:
                self.data[params] = self.data[params].combine_with(new_results)
            else:
                self.data[params] = new_results

    def to_csv(self, filename: str, parameter_names: list[str]):
        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerow([*parameter_names, *Result._fields])
            for params, result in self.data.items():
                writer.writerow([*params, *result])


def read_results(filename: str) -> Results:
    results = Results()
    if os.path.exists(filename):
        with open(filename) as f:
            next(f)
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                n_result_fields = len(Result._fields)
                results[tuple(row[:-n_result_fields])] = Result(*row[-n_result_fields:])
    return results


def update_saved_results(
    new_results: Results, filename: str, parameter_names: list[str]
):
    old_results = read_results(filename)
    new_results.update_with(old_results)
    new_results.to_csv(filename, parameter_names)


def replicate_experiment(
    sample_fnc: Callable, params: tuple, sample_size: int, seed: int = None
) -> Result:
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    sample_maxes = [sample_fnc(*params) for _ in range(sample_size)]
    return Result(np.mean(sample_maxes), sample_size)


def compute_results(sample_fnc: Callable, param_grid, sample_size: int) -> Results:
    seeds = [random.randint(0, 2**32 - 1) for _ in range(len(param_grid))]
    results = Pool().starmap(
        replicate_experiment,
        zip(repeat(sample_fnc), param_grid, repeat(sample_size), seeds),
    )
    return Results({params: result for params, result in zip(param_grid, results)})
