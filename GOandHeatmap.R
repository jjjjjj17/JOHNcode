# 加载所需的包
library(clusterProfiler)
library(enrichplot)
library(org.Hs.eg.db)  
library(GO.db)
library(AnnotationDbi)

# 设置工作目录
setwd('C:/Chinanew')

# 读取包含基因名称的 CSV 文件
data <- read.csv("ALL_gene.csv")

# 检查数据框的前几行
print(head(data))

# 提取基因列中的基因名称
gene_names <- data$Gene

# 将基因名称转换为基因ID
gene_ids <- AnnotationDbi::select(org.Hs.eg.db, 
                                  keys = gene_names, 
                                  columns = "ENTREZID", 
                                  keytype = "SYMBOL")

# 检查转换后的数据框
print(head(gene_ids))

# 移除包含 NA 的行（表示某些基因名称没有找到对应的基因ID）
gene_ids <- na.omit(gene_ids)

# 将结果转换为数据框
gene_df <- as.data.frame(gene_ids)

# 指定输出的文件路径和文件名
output_file <- "C:/China/converted_gene_idstest.csv"

# 将数据写入 CSV 文件
write.csv(gene_df, file = output_file, row.names = FALSE)

# 重新读取转换后的基因 ID 文件
data <- read.csv("converted_gene_idstest.csv")

# 提取基因 ID 列
genes <- data$ENTREZID

# 检查提取的基因 ID 列
print(head(genes))

# 进行 GO 富集分析（生物过程）
GO <- enrichGO(gene = genes, 
               OrgDb = org.Hs.eg.db, 
               keyType = "ENTREZID", 
               ont = "all",  # 仅分析生物过程（Biological Process）
               pAdjustMethod = "BH",
               pvalueCutoff = 0.05,
               qvalueCutoff = 0.05,
               readable = TRUE)

# 检查 GO 富集分析结果
print(summary(GO))

# 可视化并按照 ONTOLOGY 列分组
dotplot(GO, showCategory = 5) + facet_grid(ONTOLOGY ~ ., scale = "free")

###########################################################################################################

# 进行 GO 富集分析（生物过程）
ego_bp <- enrichGO(gene = genes, 
                   universe = genes, 
                   OrgDb = org.Hs.eg.db, 
                   keyType = "ENTREZID", 
                   ont = "BP",
                   pAdjustMethod = "BH",
                   pvalueCutoff = 0.05,
                   readable = TRUE)
# 进行 GO 富集分析（细胞组成）
ego_cc <- enrichGO(gene = genes, 
                   universe = genes, 
                   OrgDb = org.Hs.eg.db, 
                   keyType = "ENTREZID", 
                   ont = "CC",
                   pAdjustMethod = "BH",
                   pvalueCutoff = 0.05,
                   readable = TRUE)

# 进行 GO 富集分析（分子功能）
ego_mf <- enrichGO(gene = genes, 
                   universe = genes, 
                   OrgDb = org.Hs.eg.db, 
                   keyType = "ENTREZID", 
                   ont = "MF",
                   pAdjustMethod = "BH",
                   pvalueCutoff = 0.05,
                   readable = TRUE)


# 使用 barplot 可视化 GO 富集分析结果
dotplot(ego_bp, showCategory = 15)
dotplot(ego_cc, showCategory = 15)
dotplot(ego_mf, showCategory = 15)
############################################################################################################

