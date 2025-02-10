# 設定工作目錄
setwd('C:/PakNew')

# 讀取文件
data <- read.csv("proteinPakallvolcanonewtest.csv")

# 檢查數據
str(data)
summary(data)

# 庫的載入
library(ggplot2)  #用於作圖
library(ggrepel)  #用於標記

# 參數設定
FC = 2
PValue = 0.05
PvalueLimit = 1
FCLimit = 1

# 添加 sig 標籤列用於標示上調/下調
data$sig[(data$PV < -1*log10(PValue) | data$PV == "NA") | (data$FC < log2(FC)) & data$FC > -log2(FC)] <- "NotSig"
data$sig[data$PV >= -1*log10(PValue) & data$FC >= log2(FC)] <- "Up"
data$sig[data$PV >= -1*log10(PValue) & data$FC <= -log2(FC)] <- "Down"

# 選擇 FC 與 PValue 超過多少的蛋白質要標示出名字
data$label <- ifelse(data$PV > PvalueLimit & data$FC >= FCLimit & data$sig == "Up", as.character(data$Protein_Name), '')

# 繪圖
p.vol <- ggplot(data, aes(FC, PV)) +    
  geom_point(aes(color = sig), size = 1) +                           
  scale_y_continuous(limits = c(0, 10)) +
  scale_x_continuous(limits = c(-5, 5)) +
  labs(x = "log[2](FC)", y = "-log[10](PValue)") + 
  scale_color_manual(values = c("red", "grey", "blue")) + 
  geom_hline(yintercept = -log10(PValue), linetype = 2) +        
  geom_vline(xintercept = c(-log2(FC), log2(FC)), linetype = 2) +
  geom_text_repel(data = subset(data, sig %in% c("Up", "Down")), # 條件過濾，只顯示上調和下調的蛋白質名字
                  aes(x = FC, y = PV, label = ""),
                  max.overlaps = 10000,
                  size = 2.5,
                  box.padding = unit(0.5, 'lines'),
                  point.padding = unit(0.1, 'lines'), 
                  segment.color = 'black',
                  show.legend = FALSE) +
  theme(panel.grid = element_blank(),
        panel.background = element_rect(fill = "white"),
        axis.line = element_line(color = "black", size = 0.5)) 


# 檢查是否有錯誤
print(p.vol)

# 圖片保存
ggsave(p.vol, filename = "Volcano1116.pdf")

# 選擇上調的蛋白質名字的行
upregulated_proteins <- data[data$sig == "Up", c("Protein")]
#upregulated_genes<-data[data$sig == "Up", c("Gene")]
# 選擇下調的蛋白質名字的行
downregulated_proteins <- data[data$sig == "Down", c("Protein")]
#downregulated_genes<-data[data$sig == "Down", c("Gene")]
# 寫入到新的 .tsv 檔案，將路徑更改為目標目錄
write.table(upregulated_proteins, file = "C:/PakNew/upregulated_proteinalltest.csv", sep = "\t", quote = FALSE, row.names = FALSE, col.names = "Protein")
write.table(downregulated_proteins, file = "C:/PakNew/downregulated_proteinalltest.csv", sep = "\t", quote = FALSE, row.names = FALSE, col.names = "Protein")
#write.table(upregulated_genes, file = "C:/PakNew/upregulated_geneall.csv", sep = "\t", quote = FALSE, row.names = FALSE, col.names = "Gene")
#write.table(downregulated_genes, file = "C:/PakNew/downregulated_geneall.csv", sep = "\t", quote = FALSE, row.names = FALSE, col.names = "Gene")
