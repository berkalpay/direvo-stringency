library(ggplot2)

ggplot(data.frame(x=c(2,4,6,8,10), y=c(1, .289, .162, .112, .087))) +
  geom_point(aes(x=x, y=y)) +
  scale_y_continuous(breaks=seq(0, 1, 0.25), labels=c("0", "1/4", "1/2", "3/4", "1")) +
  xlab(expression(paste("Population size, ", italic(n)))) +
  ylab(expression(paste("DFE heterogeneity threshold, ", alpha,"*"))) +
  theme_classic() +
  theme(text=element_text(size=8))
ggsave("../figures/alpha_star.pdf", width=2, height=2)
