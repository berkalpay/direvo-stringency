library(readr)
library(dplyr)
library(ggplot2)

format_labels <- function(label) {
  paste0("underline(", label, ")")
}

plot_df <- read_csv("../results/evo_experiment.csv") %>%
  group_by(n, k, gen, delta_magnitude, delta_p, recover_p) %>%
  summarize(mean_max_fitness=mean(max_fitness)) %>%
  ungroup(k) %>%
  mutate(mean_max_improvement=mean_max_fitness/mean_max_fitness[which(k==1)],
         gen=as.factor(gen)) %>%
  filter(gen %in% c(5, 10, 20))

ggplot(plot_df, aes(x=k)) +
    geom_line(aes(y=mean_max_improvement, color=gen)) +
    facet_grid(delta_magnitude~delta_p,
               labeller=as_labeller(format_labels, default=label_parsed)) +
    xlab(expression(paste("Number of variants selected, ",  italic(k)))) +
    ylab("Fold improvement of average max\nfitness over max stringency") +
    labs(tag=expression(underline(paste("Decrease in DFE scale, ", italic(d))))) +
    labs(color="Number of rounds") +
    scale_y_continuous(breaks=c(1,2,3)) +
    scale_color_manual(values=c("#DDCC77", "#44AA99", "#332288")) +
    theme_classic() +
    theme(strip.text.x=element_blank(),
          strip.background=element_blank(), strip.text.y=element_text(size=11),
          plot.title=element_text(size=11, hjust=0.5),
          legend.position="bottom", legend.margin=margin(-7,0,0,0),
          plot.tag.position=c(1.02, 0.58), plot.tag=element_text(angle=270, size=11),
          plot.margin=margin(t=1, r=15, b=5, l=1))
ggsave("../figures/evo_experiment.pdf", width=5, height=3.3)
