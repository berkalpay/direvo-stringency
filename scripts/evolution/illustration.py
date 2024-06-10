import numpy as np
import matplotlib.pyplot as plt
from evolution import Variant, standard_landscape, DirectedEvolution
from experiment import run_selection_experiment


plt.rcParams["text.usetex"] = True
plt.rcParams["font.family"] = "Helvetica"
plt.rcParams["font.size"] = 13


def plot(de: DirectedEvolution, ax, n_bins=3, title="", yaxis=True):
    for generation, population in enumerate(de.populations):
        selecteds = de.selecteds[generation]
        k = len(selecteds)

        # Display the selected variants
        im = ax.scatter(
            [generation + 1] * k,
            range(1, k + 1) if generation > 0 else [1] * k,
            c=[variant.dfe_arg for variant in selecteds],
            cmap="Reds",
            vmin=0,
            vmax=de.landscape.dfe_arg_max,
            edgecolors="k",
            s=70,
            zorder=2,
        )

        # Display bins of the nonselected variants
        if generation > 0 and n_bins > 0:
            bin_indices = np.array_split(range(k, len(population)), n_bins)
            for bin_number, bin_i in enumerate(bin_indices):
                variant_bin = [population[i] for i in bin_i]
                dfe_arg_mean = np.mean([variant.dfe_arg for variant in variant_bin])
                ax.scatter(
                    [generation + 1],
                    [k + bin_number + 1],
                    c=dfe_arg_mean,
                    cmap="Reds",
                    vmin=0,
                    vmax=de.landscape.dfe_arg_max,
                    edgecolors="k",
                    s=70,
                )

        # Connect the selected variants by parentage
        if generation > 0:
            for i, variant in enumerate(selecteds):
                parent_rank = de.populations[generation - 1].index(variant.parent) + 1
                ax.plot(
                    [generation, generation + 1],
                    [parent_rank, i + 1],
                    "k-",
                    lw=0.5,
                    zorder=1,
                )

    if yaxis:
        ytick_labels = [
            *range(1, k + 1),
            *[f"{bin_i[0]+1}-{bin_i[-1]+1}" for bin_i in bin_indices],
        ]
        ax.set_yticks(range(1, k + n_bins + 1))
        ax.set_yticklabels(ytick_labels)
        ax.set_ylabel("Fitness rank")
    else:
        ax.get_yaxis().set_visible(False)
    ax.invert_yaxis()

    ax.get_xaxis().set_visible(False)
    ax.tick_params(axis="y", left=False)
    [spine.set_visible(False) for spine in ax.spines.values()]
    ax.set_title(title)

    return im


if __name__ == "__main__":

    def example_de(delta_p, delta_magnitude, recover_p=0, n_gen=4, k=5):
        return run_selection_experiment(
            Variant(0, 1),
            pop_size=100,
            landscape=standard_landscape(delta_magnitude, delta_p, recover_p),
            n_to_select=k,
            n_gen=n_gen,
            seed=1,
            mutagenesis_sampling="exact",
        )

    de1 = example_de(0.1, 0.5)
    de2 = example_de(0.5, 0.5)
    de3 = example_de(0.8, 0.5)

    fig, axes = plt.subplots(1, 3, figsize=(7.5, 2.75))
    plot(de1, axes[0], title=r"\underline{0.1}")
    axes[0].yaxis.label.set_size(15)
    plot(de2, axes[1], title=r"\underline{0.5}", yaxis=False)
    im = plot(de3, axes[2], title=r"\underline{0.8}", yaxis=False)
    plt.tight_layout()

    fig.subplots_adjust(right=0.9, top=0.8)
    cax = fig.add_axes([0.93, 0.08, 0.01, 0.7])
    cbar = fig.colorbar(im, cax=cax, ticks=[0, 1 / 3, 2 / 3, 1])
    cbar.set_ticklabels(["0", "1/3", "2/3", "1"])
    for label in cbar.ax.yaxis.get_ticklabels()[1:-1]:
        label.set_visible(False)
    cbar.ax.set_ylabel(r"$\beta$", rotation=0)
    fig.suptitle(r"\underline{Probability of decrease in DFE scale, $p$", y=1)

    plt.show()
    fig.savefig("figures/evo_short_illustration.pdf")

    de4 = example_de(0.5, 0.5, 0.05, 19, 2)
    fig, axes = plt.subplots(3, 1, figsize=(8, 5.7))
    plot(de4, axes[1])
    axes[1].set_ylabel("k=2", rotation=270)
    axes[1].yaxis.label.set_color("olive")
    axes[1].yaxis.set_label_position("right")
    axes[0].plot(range(20), [de4.max_fitness(i) for i in range(20)], c="olive")

    de5 = example_de(0.5, 0.5, 0.05, 19)
    plot(de5, axes[2])
    axes[2].set_ylabel("k=5", rotation=270)
    axes[2].yaxis.label.set_color("teal")
    axes[2].yaxis.set_label_position("right")
    axes[0].plot(range(20), [de5.max_fitness(i) for i in range(20)], c="teal")

    supy = fig.supylabel("Fitness rank", family="Arial")
    supy.set_position((supy.get_position()[0], 0.35))
    supy.set_fontsize(axes[2].get_yaxis().get_label().get_fontsize())

    axes[0].get_xaxis().set_visible(False)
    axes[0].set_yticks([])
    axes[0].tick_params(axis="y", left=False)
    axes[0].set_ylabel("Maximum fitness")
    [spine.set_visible(False) for spine in axes[0].spines.values()]
    plt.tight_layout()

    fig.subplots_adjust(bottom=0.1)
    cax = fig.add_axes([0.2, 0.05, 0.7, 0.02])
    cbar = fig.colorbar(
        im, cax=cax, orientation="horizontal", ticks=[0, 1 / 3, 2 / 3, 1]
    )
    cbar.set_ticklabels(["0", "1/3", "2/3", "1"])
    for label in cbar.ax.xaxis.get_ticklabels()[1:-1]:
        label.set_visible(False)
    cbar.ax.set_ylabel(r"$\beta$", rotation=0, labelpad=15)
    cbar.ax.yaxis.set_label_position("right")

    plt.show()
    fig.savefig("figures/evo_long_illustration.pdf")
