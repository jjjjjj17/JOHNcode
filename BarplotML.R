library(ggplot2)
library(dplyr)
library(tidyr)

importance_df <- read.csv("C:/China/top_10_features_importance_matrix1.csv")

importance_long <- importance_df %>%
  pivot_longer(cols = -Protein, names_to = "Method", values_to = "Importance")

importance_total <- importance_long %>%
  group_by(Protein) %>%
  summarize(Total_Importance = sum(Importance, na.rm = TRUE)) %>%
  arrange(Total_Importance)

importance_long <- importance_long %>%
  mutate(Protein = factor(Protein, levels = importance_total$Protein))

custom_colors <- c(
  "Logistic_Regression" = "cadetblue3",  
  "XGBoost" = "#8a7eb0",              
  "SVM" = "#ff9f9d",                 
  "Random_Forest" = "aquamarine2",       
  "AdaBoost" = "#ffcc66",           
  "MLP" = "azure4"                  
)

ggplot(importance_long, aes(x = Protein, y = Importance, fill = Method)) +
  geom_bar(stat = "identity") +
  coord_flip() +
  theme_minimal() +
  labs(title = "Top 10 Protein Importance by Machine Learning Methods",
       x = "Protein",
       y = "Importance",
       fill = "Method") +
  scale_fill_manual(values = custom_colors)
