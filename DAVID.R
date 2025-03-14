# 加载必要的包
library(ggplot2)
library(dplyr)
library(tidyr)

setwd('C:/China')

david_data <- read.csv("david_kegg_results.csv")

david_data <- david_data %>%
  mutate(GeneRatio = Count / Listtotal)

plot_data <- david_data %>%
  select(Term, Count, PValue, FoldEnrichment, Listtotal, GeneRatio) %>%
  mutate(PValue = -log10(PValue)) %>%
  arrange(desc(GeneRatio))  

print(head(plot_data))

ggplot(plot_data, aes(x = GeneRatio, y = reorder(Term, GeneRatio))) +
  geom_point(aes(size = Count, color = PValue)) +
  scale_size_continuous(name = "Count") +
  scale_color_gradient(low = "blue", high = "red", name = "-log10(PValue)") +
  labs(
    x = "GeneRatio",
    y = "KEGG Pathway"
  ) +
  theme_minimal() +
  theme(
    panel.border = element_rect(color = "black", fill = NA, size = 0.5),
    # 设置坐标轴的颜色和粗细
    axis.ticks = element_line(color = "black", size = 1),  # 设置刻度线的颜色和粗细
    axis.text.x = element_text(size = 13, face = "bold"),  # 调整x轴刻度标签的大小和样式
    axis.text.y = element_text(size = 13, face = "bold"),
    plot.title = element_text(size = 13, face = "bold", hjust = 0.5),
    axis.title = element_text(size = 13, face = "bold")
  )
