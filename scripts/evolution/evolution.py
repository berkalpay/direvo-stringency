import math
import itertools
from dataclasses import dataclass
from typing import NamedTuple, List, Callable
import numpy as np


class Variant(NamedTuple):
    fitness: float
    dfe_arg: float
    parent: "Variant" = None


@dataclass(frozen=True)
class Landscape:
    dfe: Callable
    delta_magnitude: float
    delta_p: float
    recover_p: float = 0
    dfe_arg_min: float = -math.inf
    dfe_arg_max: float = math.inf

    def delta_dfe_arg(self, size: int):
        return np.random.default_rng().choice(
            [-self.delta_magnitude, 0, 1],
            size,
            p=[self.delta_p, 1 - self.delta_p - self.recover_p, self.recover_p],
        )

    def generate_dfe_args(self, dfe_args: List[float]):
        return np.clip(
            np.array(dfe_args) + self.delta_dfe_arg(size=len(dfe_args)),
            self.dfe_arg_min,
            self.dfe_arg_max,
        )

    def generate_children(self, variant: Variant, n: int) -> List[Variant]:
        fitnesses = [
            variant.fitness + effect for effect in self.dfe(variant.dfe_arg, size=n)
        ]
        dfe_args = self.generate_dfe_args([variant.dfe_arg] * n)
        return [
            Variant(fitness, dfe_arg, variant)
            for fitness, dfe_arg in zip(fitnesses, dfe_args)
        ]


def standard_landscape(
    delta_magnitude: float, delta_p: float, recover_p: float = 0
) -> Landscape:
    dfe = np.random.default_rng().exponential
    return Landscape(dfe, delta_magnitude, delta_p, recover_p, 0.01, 1)


def sorted_by_fitness(population: List[Variant]) -> List[Variant]:
    return sorted(population, key=lambda x: x.fitness, reverse=True)


class DirectedEvolution:
    def __init__(self, initial_pop: List[Variant], landscape: Landscape):
        self.landscape = landscape
        self.populations = [sorted_by_fitness(initial_pop)]
        self.selecteds = []
        self.pop_size = len(initial_pop)

    def __len__(self):
        return len(self.populations)

    def mutagenize(self, sampling: str = "multinomial") -> None:
        selecteds = self.selecteds[-1]
        k = len(selecteds)
        if sampling == "multinomial":
            n_children = np.random.default_rng().multinomial(self.pop_size, [1 / k] * k)
        elif sampling == "exact":
            assert self.pop_size % k == 0
            n_children = [self.pop_size // k] * k
        children = [
            self.landscape.generate_children(variant, nc)
            for variant, nc in zip(selecteds, n_children)
        ]
        pop = list(itertools.chain.from_iterable(children))
        self.populations.append(sorted_by_fitness(pop))

    def select(self, n: int) -> None:
        self.selecteds.append(self.populations[-1][:n])

    def max_fitness(self, generation: int = -1) -> float:
        return self.populations[generation][0].fitness

    def run(
        self, n_to_select: int, n_gen: int, mutagenesis_sampling="multinomial"
    ) -> None:
        assert n_gen > 0
        for _ in range(n_gen):
            if len(self.selecteds) < len(self.populations):
                self.select(n_to_select)
            self.mutagenize(mutagenesis_sampling)
        self.select(n_to_select)
