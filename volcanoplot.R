# 設定工作目錄
setwd('C:/Dutch')

data <- read.csv("Ducvolcanotest.csv")

str(data)
summary(data)

library(ggplot2)  #用於作圖
library(ggrepel)  #用於標記

FC = 2
PValue = 0.05
PvalueLimit = 1
FCLimit = 1

data$sig[(data$PV < -1*log10(PValue) | data$PV == "NA") | (data$FC < log2(FC)) & data$FC > -log2(FC)] <- "NotSig"
data$sig[data$PV >= -1*log10(PValue) & data$FC >= log2(FC)] <- "Up"
data$sig[data$PV >= -1*log10(PValue) & data$FC <= -log2(FC)] <- "Down"

data$label <- ifelse(data$PV > PvalueLimit & data$FC >= FCLimit & data$sig == "Up", as.character(data$Protein_Name), '')

p.vol <- ggplot(data, aes(x = FC, y = PV)) +    
  geom_point(aes(fill = sig, color = sig), size = 3, alpha = 0.6, stroke = 1.5, shape = 21) +  
  scale_y_continuous(limits = c(0, 5)) +
  scale_x_continuous(limits = c(-10, 10)) +
  labs(x = "log[2](FC)", 
       y = "-log[10](PValue)") + 
  scale_fill_manual(values = c("lightblue", "lightgrey", "lightcoral")) + 
  scale_color_manual(values = c("blue", "grey", "red")) +  # 边线颜色
  geom_hline(yintercept = -log10(PValue), linetype = 2) +        
  geom_vline(xintercept = c(-log2(FC), log2(FC)), linetype = 2) + 
  geom_text_repel(aes(x = FC,                   
                      y = PV,          
                      label = label),                       
                  max.overlaps = 10000, 
                  size = 2.5, 
                  box.padding = unit(0.5, 'lines'), 
                  point.padding = unit(0.1, 'lines'), 
                  segment.color = 'black', 
                  show.legend = FALSE) + 
  theme(panel.grid = element_blank(),                      
        panel.background = element_rect(fill = "white"),
        axis.line = element_line(color = "black", size = 0.5),
        axis.title.x = element_text(size = 14),            
        axis.title.y = element_text(size = 14),            
        axis.text.x = element_text(size = 12),           
        axis.text.y = element_text(size = 12),            
        legend.text = element_text(size = 12),            
        legend.title = element_text(size = 14)) 
print(p.vol)
ggsave(p.vol, filename = "Volcano1116_China.pdf")

upregulated_proteins <- data[data$sig == "Up", c("Protein")]

downregulated_proteins <- data[data$sig == "Down", c("Protein")]

write.table(upregulated_proteins, file = "C:/Dutch/upregulated_proteintest.csv", sep = "\t", quote = FALSE, row.names = FALSE, col.names = "Protein")
write.table(downregulated_proteins, file = "C:/Dutch/downregulated_proteintest.csv", sep = "\t", quote = FALSE, row.names = FALSE, col.names = "Protein")
write.table(upregulated_genes, file = "C:/Dutch/upregulated_gene.csv", sep = "\t", quote = FALSE, row.names = FALSE, col.names = "Gene")
write.table(downregulated_genes, file = "C:/Dutch/downregulated_gene.csv", sep = "\t", quote = FALSE, row.names = FALSE, col.names = "Gene")
