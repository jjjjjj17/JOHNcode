library(rio)
library(dplyr)


combined_data <- import('C:/China/Chinaprotein.txt')
cols <- c("Protein","Gene","RA11", "RA12", "RA13","RA21","RA22","RA23","RA31","RA32","RA33","RA41","RA42","RA43","RA51","RA52","RA53","RA61","RA62","RA63","RA71","RA72","RA73","control11", "control12","control13","control21","control22", "control23","control31", "control32","control33","control41","control42","control43", "control51","control52","control53","control61", "control62","control63","control71", "control72","control73","control81","control82","control83")
d1_data <- data.frame(matrix(NA, nrow = nrow(combined_data), ncol = length(cols)))
colnames(d1_data) <- cols
d1_data$Protein <- combined_data$`Entry Name`
d1_data$Gene <- combined_data$`Gene`
d1_data$RA11 <- combined_data$`R1_1 Intensity`
d1_data$RA12 <- combined_data$`R1_2 Intensity`
d1_data$RA13 <- combined_data$`R1_3 Intensity`
d1_data$RA21 <- combined_data$`R2_1 Intensity`
d1_data$RA22 <- combined_data$`R2_2 Intensity`
d1_data$RA23 <- combined_data$`R2_3 Intensity`
d1_data$RA31 <- combined_data$`R3_1 Intensity`
d1_data$RA32 <- combined_data$`R3_2 Intensity`
d1_data$RA33 <- combined_data$`R3_3 Intensity`
d1_data$RA41 <- combined_data$`R4_1 Intensity`
d1_data$RA42 <- combined_data$`R4_2 Intensity`
d1_data$RA43 <- combined_data$`R4_3 Intensity`
d1_data$RA51 <- combined_data$`R5_1 Intensity`
d1_data$RA52 <- combined_data$`R5_2 Intensity`
d1_data$RA53 <- combined_data$`R5_3 Intensity`
d1_data$RA61 <- combined_data$`R6_1 Intensity`
d1_data$RA62 <- combined_data$`R6_2 Intensity`
d1_data$RA63 <- combined_data$`R6_3 Intensity`
d1_data$RA71 <- combined_data$`R7_1 Intensity`
d1_data$RA72 <- combined_data$`R7_2 Intensity`
d1_data$RA73 <- combined_data$`R7_3 Intensity`
d1_data$control11 <- combined_data$`C1_1 Intensity`
d1_data$control12 <- combined_data$`C1_2 Intensity`
d1_data$control13 <- combined_data$`C1_3 Intensity`
d1_data$control21 <- combined_data$`C2_1 Intensity`
d1_data$control22 <- combined_data$`C2_2 Intensity`
d1_data$control23 <- combined_data$`C2_3 Intensity`
d1_data$control31 <- combined_data$`C3_1 Intensity`
d1_data$control32 <- combined_data$`C3_2 Intensity`
d1_data$control33 <- combined_data$`C3_3 Intensity`
d1_data$control41 <- combined_data$`C4_1 Intensity`
d1_data$control42 <- combined_data$`C4_2 Intensity`
d1_data$control43 <- combined_data$`C4_3 Intensity`
d1_data$control51 <- combined_data$`C5_1 Intensity`
d1_data$control52 <- combined_data$`C5_2 Intensity`
d1_data$control53 <- combined_data$`C5_3 Intensity`
d1_data$control61 <- combined_data$`C6_1 Intensity`
d1_data$control62 <- combined_data$`C6_2 Intensity`
d1_data$control63 <- combined_data$`C6_3 Intensity`
d1_data$control71 <- combined_data$`C7_1 Intensity`
d1_data$control72 <- combined_data$`C7_2 Intensity`
d1_data$control73 <- combined_data$`C7_3 Intensity`
d1_data$control81 <- combined_data$`C8_1 Intensity`
d1_data$control82 <- combined_data$`C8_2 Intensity`
d1_data$control83 <- combined_data$`C8_3 Intensity`
# Replace 0 values with NA
# 去掉含有NA值的行
d2 <- na.omit(d1_data)

# 转换为数据框（如果还不是）
d2 <- as.data.frame(d2)

# 将结果写入CSV文件
write.csv(d2, file = "C:/China/proteinChinanew.csv", row.names = FALSE)

# 检查d2的结构
print(str(d2))

# 检查d2的前几行
print(head(d2))