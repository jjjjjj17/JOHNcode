

# 读取包含数据的CSV文件，文件名为 your_data.csv
data <- read.csv("C:/China/China_normalizenew.csv", header=TRUE)

x1 <- 3
x2 <- 23
y1 <- 24
y2 <- 47


# Calculate -log10-transformed PV
data$PV <- sapply(1:nrow(data), function(i) {
  pv_value <- as.numeric(as.character(t.test(as.numeric(as.character(unlist(data[i,x1:x2]))), as.numeric(as.character(unlist(data[i,y1:y2]))))[c("p.value")]))
  -log10(pv_value)
})

# Calculate log2-transformed FC
data$FC <- sapply(1:nrow(data), function(i) {
  fc_value <- mean(as.numeric(as.character(data[i,x1:x2])))/mean(as.numeric(as.character(data[i,y1:y2])))
  log2(fc_value)
})
write.csv(data, file = "C:/China/Chinavolcanonew.csv", row.names = FALSE)
d1_data <- read.csv("C:/China/Chinavolcanonew.csv", header=TRUE)


# Replace 0 values with NA
d1_data[d1_data == Inf] <- NA
d1_data[d1_data == -Inf] <- NA
# Remove rows with NA
print(d1_data)
d1_data <- na.omit(d1_data)

# Convert to data frame (if not already)
d1_data <- as.data.frame(d1_data)
write.csv(d1_data, file = "C:/China/Chinavolcanonew.csv", row.names = FALSE)
