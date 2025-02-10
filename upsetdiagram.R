# 加载所需的包
library(UpSetR)

# 读取 CSV 文件
file_paths <- c(
  "C:/Chinanew/top_15_features.csv",
  "C:/Chinanew/top_15_features1.csv",
  "C:/Chinanew/top_15_features2.csv",
  "C:/Chinanew/top_15_features3.csv",
  "C:/Chinanew/top_15_features4.csv",
  "C:/Chinanew/top_15_features5.csv",
  "C:/Chinanew/ALL_protein.csv"
)

data_list <- lapply(file_paths, read.csv)

# 确保蛋白质列存在并且没有 NA 值
protein_names_list <- lapply(data_list, function(df) na.omit(df[, 1]))

# 打印以检查数据是否正确读取
lapply(protein_names_list, head)

# 合并所有蛋白质名称
all_proteins <- unique(unlist(protein_names_list))

# 检查是否存在空值
all_proteins <- na.omit(all_proteins)

# 创建一个二进制矩阵
protein_matrix <- data.frame(
  XGBoost = as.numeric(all_proteins %in% protein_names_list[[1]]),
  Random_Forest = as.numeric(all_proteins %in% protein_names_list[[2]]),
  AdaBoost = as.numeric(all_proteins %in% protein_names_list[[3]]),
  SVM = as.numeric(all_proteins %in% protein_names_list[[4]]),
  MLP = as.numeric(all_proteins %in% protein_names_list[[5]]),
  Logistic_Regression = as.numeric(all_proteins %in% protein_names_list[[6]]),
  DEP = as.numeric(all_proteins %in% protein_names_list[[7]]),
  row.names = all_proteins
)

# 打印矩阵以检查数据
print(head(protein_matrix))

# 查找包含所有方法的蛋白质
all_methods_protein <- rownames(protein_matrix[rowSums(protein_matrix) == 7, ])
print(all_methods_protein)

# 查找包含6种方法的蛋白质
six_methods_protein <- rownames(protein_matrix[rowSums(protein_matrix) == 6, ])
print(six_methods_protein)

# 使用手动排序确保包含所有方法的蛋白质在图中单独显示
protein_matrix <- protein_matrix[order(rowSums(protein_matrix), decreasing = TRUE), ]

# 保存为 PDF 文件
pdf(file = "C:/Chinanew/UpSet_plot.pdf", width = 12, height = 8) # 调整宽度和高度

upset(
  protein_matrix, 
  sets = c("XGBoost", "Random_Forest", "AdaBoost", "SVM", "MLP", "Logistic_Regression", "DEP"), 
  order.by = "freq", 
  main.bar.color = "darkblue", 
  sets.bar.color = "brown", 
  text.scale = c(2, 2, 1.5, 1.5),
  keep.order = TRUE,  # 保持原始顺序
  nintersects = 60  # 显示的最大交集数量，确保所有交集显示
)

dev.off() # 关闭 PDF 设备

# 提取所有交集的蛋白质
intersection_data <- data.frame(Feature = rownames(protein_matrix))
intersection_data$Intersection <- apply(protein_matrix, 1, function(row) {
  present_sets <- names(which(row == 1))
  paste(present_sets, collapse = ", ")
})

# 打印具有交集的蛋白质和它们的集合
print(intersection_data)

# 输出结果到 CSV 文件
output_file <- "C:/Chinanew/MLintersection_data.csv"
write.csv(intersection_data, file = output_file, row.names = FALSE)

##############################################################################
# 加载所需的包
library(UpSetR)

# 读取四个CSV文件
file1 <- "C:/Chinanew/ALL_protein.csv"
file2 <- "C:/Dutch/ALL_protein.csv"
file3 <- "C:/China/ALL_protein.csv"
file4 <- "C:/Paknew/ALL_protein.csv"

data1 <- read.csv(file1)
data2 <- read.csv(file2)
data3 <- read.csv(file3)
data4 <- read.csv(file4)

protein_names1 <- na.omit(data1$Protein)
protein_names2 <- na.omit(data2$Protein)
protein_names3 <- na.omit(data3$Protein)
protein_names4 <- na.omit(data4$Protein)


print(head(protein_names1))
print(head(protein_names2))
print(head(protein_names3))
print(head(protein_names4))

# 合并所有蛋白质名称
all_proteins <- unique(c(protein_names1, protein_names2, protein_names3, protein_names4))

# 检查是否存在空值
all_proteins <- na.omit(all_proteins)

# 创建一个二进制矩阵
protein_matrix <- data.frame(
  China_Beijing = as.numeric(all_proteins %in% protein_names1),
  Dutch = as.numeric(all_proteins %in% protein_names2),
  China_GuangZhou = as.numeric(all_proteins %in% protein_names3),
  Pakistani = as.numeric(all_proteins %in% protein_names4),
  row.names = all_proteins
)

# 打印矩阵以检查数据
print(head(protein_matrix))

# 绘制UpSet图
upset(
  protein_matrix, 
  sets = c("China_Beijing", "Dutch", "China_GuangZhou", "Pakistani"), 
  order.by = "freq", 
  main.bar.color = "darkblue", 
  sets.bar.color = "brown", 
  text.scale = c(2, 2, 1.5, 1.5)
)

# 提取所有交集的蛋白质
intersection_data <- data.frame(Protein = rownames(protein_matrix))
intersection_data$Intersection <- apply(protein_matrix, 1, function(row) {
  present_sets <- names(which(row == 1))
  paste(present_sets, collapse = ", ")
})

# 打印具有交集的蛋白质和它们的集合
print(intersection_data)

# 输出结果到CSV文件
output_file <- "C:/Chinanew/intersection_data.csv"
write.csv(intersection_data, file = output_file, row.names = FALSE)

