# 加载必要的包
library(ggplot2)
library(dplyr)
library(tidyr)

setwd('C:/PakNew')

# 读取数据
david_gobp <- read.csv("david_gobp_results.csv")
david_gocc <- read.csv("david_gocc_results.csv")
david_gomf <- read.csv("david_gomf_results.csv")

david_gobp <- david_gobp %>% mutate(Ontology = "BP")
david_gocc <- david_gocc %>% mutate(Ontology = "CC")
david_gomf <- david_gomf %>% mutate(Ontology = "MF")

david_data <- bind_rows(david_gobp, david_gocc, david_gomf)

david_data <- david_data %>%
  mutate(GeneRatio = Count / Listtotal)

plot_data <- david_data %>%
  select(Term, Count, PValue, FoldEnrichment, Listtotal, GeneRatio, Ontology) %>%
  mutate(PValue = -log10(PValue)) %>%
  arrange(desc(GeneRatio))  
plot_data <- plot_data %>%
  filter(!is.na(Term) & !is.na(GeneRatio) & !is.na(PValue))

ggplot(plot_data, aes(x = GeneRatio, y = reorder(Term, GeneRatio), color = PValue, size = Count)) +
  geom_point() +
  scale_size_continuous(name = "Count") +
  scale_color_gradient(low = "blue", high = "red", name = "-log10(PValue)") +
  labs(
    x = "GeneRatio",
    y = "Pathway",  # 设置 y 轴标签
   
  ) +
  theme_minimal() +
  theme(
    axis.text.y = element_text(size = 13, face = "bold"),  # 加粗 Term（Pathway 名称）
    axis.text.x = element_text(size = 13, face = "bold"),
    axis.title = element_text(size = 13, face = "bold"),
    plot.title = element_text(size = 13, face = "bold", hjust = 0.5),
    panel.border = element_rect(color = "black", fill = NA, size = 0.5),
    axis.ticks = element_line(color = "black", size = 0.5),  # 设置刻度线的颜色和粗细
    strip.background = element_rect(color = "black", fill = NA, size = 0.5),
    strip.text.x = element_text(size = 13, face = "bold")
  ) +
  facet_grid(Ontology ~ ., scales = "free", space = "free_y")
