# 加载所需的包
library(ggplot2)
library(ggpubr)
library(dplyr)
library(tidyr)

# 读取 CSV 文件
file_paths <- c(
  "C:/Chinanew/atop_15_features5.csv",
  "C:/Chinanew/atop_15_features.csv",
  "C:/Chinanew/atop_15_features3.csv",
  "C:/Chinanew/atop_15_features1.csv",
  "C:/Chinanew/atop_15_features2.csv",
  "C:/Chinanew/atop_15_features4.csv"
)

# 读取所有数据文件
data_list <- lapply(file_paths, read.csv)

# 定义机器学习方法的名称
methods <- c("Logistic_Regression","XGBoost", "SVM", "Random_Forest", "AdaBoost", "MLP")

# 定义蛋白质名称
proteins <- c("FA9_HUMAN", "A2GL_HUMAN", "APOF_HUMAN", "SAA1_HUMAN", "FETUB_HUMAN")

# 创建一个空的数据框用于存储整理后的数据
importance_data <- data.frame()

# 提取每个蛋白质的 Importance 值并存储到数据框中
for (i in 1:length(data_list)) {
  method_data <- data_list[[i]]
  
  for (protein in proteins) {
    protein_importance <- method_data$Importance[method_data$Feature == protein]
    if (length(protein_importance) == 0) {
      protein_importance <- NA
    }
    
    importance_data <- rbind(importance_data, data.frame(Method = methods[i], Protein = protein, Importance = protein_importance))
  }
}

# 将数据框整理成适当的格式
importance_data <- importance_data %>% 
  filter(!is.na(Importance))

# 计算每个蛋白质的重要性平均值
protein_means <- importance_data %>%
  group_by(Protein) %>%
  summarize(Mean_Importance = mean(Importance, na.rm = TRUE))

# 将平均值作为一列添加到方法列表中
score_data <- protein_means %>%
  mutate(Method = "Score") %>%
  rename(Importance = Mean_Importance) %>%
  select(Method, Protein, Importance)

# 确保 score_data 和 importance_data 具有相同的列数和名称
importance_data <- bind_rows(importance_data, score_data)

# 计算每个蛋白质的重要性平均值并创建一个因子级别的排序
score_data <- protein_means %>%
  mutate(Method = "Score") %>%
  rename(Importance = Mean_Importance) %>%
  select(Method, Protein, Importance) %>%
  arrange(Importance) # 从小到大排序，确保最大值在底部

# 根据蛋白质的平均重要性值对蛋白质进行排序
importance_data <- importance_data %>%
  mutate(Protein = factor(Protein, levels = score_data$Protein)) %>%
  filter(!is.na(Importance)) # 确保没有NA值影响图形

# 将 Method 因子级别进行重新排序，使得 Score 位于最右侧
importance_data$Method <- factor(importance_data$Method, levels = c(methods, "Score"))

# 自定义颜色渐变
my_cols <- c("blue", "cyan", "green", "yellow", "orange", "red")

pdf(file = "C:/Chinanew/Balloon_plot_with_mean.pdf", width = 12, height = 8) # 调整宽度和高度

ggballoonplot(importance_data, x = "Method", y = "Protein", size = "Importance", fill = "Importance") +
  geom_point(aes(size = Importance), data = filter(importance_data, Method == "Score"), shape = 1, color = "black") +  # 在图中添加平均重要性
  scale_size_continuous(range = c(1, 20), breaks = seq(0, max(importance_data$Importance, na.rm = TRUE), by = 0.1)) +
  scale_fill_gradientn(colors = my_cols) +
  theme_minimal() +
  labs(title = "Balloon Plot of Protein Importance Across ML Methods",
       x = "Machine Learning Method",
       y = "Protein",
       size = "Importance",
       fill = "Importance") +
  theme(
    axis.text.x = element_text(margin = margin(t = 10)),
    axis.text.y = element_text(size = 10) # 调整Y轴文本大小以便于阅读
  )

dev.off() # 关闭 PDF 设备

#############################################################################
# 定义蛋白质名称
proteins <- c("FA9_HUMAN", "A2GL_HUMAN", "APOF_HUMAN", "SAA1_HUMAN", "HPT_HUMAN")

# 创建一个空的数据框用于存储整理后的数据
importance_data <- data.frame()

# 提取每个蛋白质的 Importance 值并存储到数据框中
for (i in 1:length(data_list)) {
  method_data <- data_list[[i]]
  
  for (protein in proteins) {
    protein_importance <- method_data$Importance[method_data$Feature == protein]
    if (length(protein_importance) == 0) {
      protein_importance <- NA
    }
    
    importance_data <- rbind(importance_data, data.frame(Method = methods[i], Protein = protein, Importance = protein_importance))
  }
}

# 将数据框整理成适当的格式
importance_data <- importance_data %>% 
  filter(!is.na(Importance))

# 计算每个蛋白质的重要性平均值
protein_means <- importance_data %>%
  group_by(Protein) %>%
  summarize(Mean_Importance = mean(Importance, na.rm = TRUE))

# 添加平均重要性到原数据框
importance_data <- left_join(importance_data, protein_means, by = "Protein")

# 将平均值作为一列添加到方法列表中
score_data <- protein_means %>%
  mutate(Method = "Score") %>%
  rename(Importance = Mean_Importance) %>%
  select(Method, Protein, Importance)

# 将分数数据添加到原始数据框中
importance_data <- rbind(importance_data, score_data)

# 根据平均值对蛋白质进行排序
importance_data <- importance_data %>%
  mutate(Protein = factor(Protein, levels = protein_means$Protein[order(-protein_means$Mean_Importance)]))

# 自定义颜色渐变
my_cols <- c("blue", "white", "red")

# 保存为 PDF 文件
pdf(file = "C:/Chinanew/Balloon_plot_with_mean.pdf", width = 12, height = 8) # 调整宽度和高度

# 绘制 Balloon Plot，交换 X 轴和 Y 轴，并根据平均值排序蛋白质
ggballoonplot(importance_data, x = "Method", y = "Protein", size = "Importance", fill = "Importance") +
  geom_point(aes(size = Importance), data = filter(importance_data, Method == "Score"), shape = 1, color = "black") +  # 在图中添加平均重要性
  scale_size(range = c(3, 15)) +
  scale_fill_gradientn(colors = my_cols) +
  theme_minimal() +
  labs(title = "Balloon Plot of Protein Importance Across ML Methods",
       x = "Machine Learning Method",
       y = "Protein",
       size = "Importance",
       fill = "Importance") +
  theme(
    axis.text.x = element_text(margin = margin(t = 10))
  )

dev.off() # 关闭 PDF 设备
