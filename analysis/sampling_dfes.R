library(readr)
library(dplyr)
library(ggplot2)

# Set common plotting parameters
font_size <- 14
theme_set(theme_bw())
theme_update(panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
             strip.background=element_blank(),
             legend.position="bottom", legend.margin=margin(-7,0,0,0),
             panel.border=element_rect(linewidth=1),
             plot.title=element_text(size=font_size, hjust=0.5, margin=margin()),
             text=element_text(size=font_size))
with_common_elements <- function(plot) {
  plot +
    geom_line(aes(color=n)) +
    facet_grid(~alpha) +
    labs(color=expression(paste("Population size, ", italic(n)))) +
    scale_x_continuous(breaks=seq(0, 1, 1/3), labels=c("0", "1/3", "2/3", "1"),
                       expand=c(0.01,0.01)) +
    ggtitle(expression(paste("DFE heterogeneity parameter, ", alpha))) +
    scale_color_manual(values=c("#9dcf8a", "#46AEA0", "#00718B"))
}

# Sampling two distributions
plot_df <- read_csv("../results/sampling_two_dfes.csv") %>%
  mutate(nlow_frac=n_low/n) %>%
  rename(mean_maxes=mean) %>%
  group_by(alpha, n) %>%
  mutate(improvement=mean_maxes-mean_maxes[which(nlow_frac==0)],
         n=as.factor(n))
p <- ggplot(plot_df, aes(x=nlow_frac, y=improvement)) +
  geom_hline(yintercept=0, linetype="dashed") +
  xlab(expression(paste("Fraction of ", italic(n), " assigned to less-fit genotype, ",
                        italic(n)[low]/italic(n)))) +
  ylab("Increase in average log max\nfitness over max stringency")
ggsave("../figures/sampling_two_dfes.pdf", with_common_elements(p), width=6, height=3)

# Sampling multiple distributions
plot_df <- read_csv("../results/sampling_multiple_dfes.csv") %>%
  rename(mean_maxes=mean) %>%
  group_by(alpha, n) %>%
  mutate(improvement=mean_maxes-mean_maxes[which(k==1)],
         k_frac=k/n,
         n=as.factor(n))
p <- ggplot(plot_df, aes(x=k_frac, y=improvement)) +
  geom_hline(yintercept=0, linetype="dashed") +
  xlab(expression(paste("Fraction of variants selected, ", italic(k)/italic(n)))) +
  ylab("Increase in average log max\nfitness over max stringency")
ggsave("../figures/sampling_multiple_dfes.pdf", with_common_elements(p), width=6, height=3)

# Sampling multiple distributions (alternative)
plot_df <- read_csv("../results/sampling_multiple_dfes_alt.csv") %>%
  rename(mean_maxes=mean) %>%
  group_by(alpha, n) %>%
  mutate(improvement=mean_maxes/mean_maxes[which(k==1)],
         k_frac=k/n,
         n=as.factor(n))
p <- ggplot(plot_df, aes(x=k_frac, y=improvement)) +
  geom_hline(yintercept=1, linetype="dashed") +
  scale_y_continuous(breaks=c(1, 3/2, 2), labels=c("1", "1.5", "2")) +
  xlab(expression(paste("Fraction of variants selected, ", italic(k)/italic(n)))) +
  ylab("Fold improvement of max\nfitness over max stringency")
ggsave("../figures/sampling_multiple_dfes_alt.pdf", with_common_elements(p), width=6, height=3)
