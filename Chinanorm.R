# 读取包含数据的CSV文件，文件名为 your_data.csv
data <- read.csv("C:/China/Modified_China.csv", header=TRUE)

# 要标准化的列的索引，假设是从第4列到第9列
columns_to_normalize <- 3:47

# 提取第4到第9列的数据
columns_data <- data[, columns_to_normalize]
columns_data <- na.omit(columns_data)

# 计算每一列的最大值和最小值
max_values <- apply(columns_data, 2, max)
min_values <- apply(columns_data, 2, min)

# 进行最小-最大标准化的计算
normalized_columns <- (columns_data - min_values) / (max_values - min_values)

# 将标准化后的数据更新回数据框
data[, columns_to_normalize] <- normalized_columns

# 将结果写入新的CSV文件
write.csv(data, file = "C://China//China_normalizenew.csv", row.names = FALSE)