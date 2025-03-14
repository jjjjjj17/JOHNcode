# 设置工作目录
setwd("C:/Chinanew")

data <- read.csv("heatmapdata_score_modified.csv", header = TRUE, row.names = 1)

data_matrix <- as.matrix(data)

library(ComplexHeatmap)
library(circlize)

candy_colors <- colorRamp2(c(-2, 0, 2), c("blue", "white", "firebrick3"))

split_point <-1

n_rows <- nrow(data_matrix)
n_cols <- ncol(data_matrix)

row_splits <- rep(1, n_rows)
row_splits[split_point:n_rows] <- 2

col_splits <- rep(1, n_cols)
col_splits[1] <- 0 


Heatmap(data_matrix,
        name = "expression",         
        col = candy_colors,          
        cluster_rows = FALSE,        
        cluster_columns = FALSE,     
        row_split = row_splits,      
        column_split = col_splits,   
        show_row_names = TRUE,      
        show_column_names = TRUE,    
        clustering_distance_rows = "euclidean",  
        clustering_method_rows = "ward.D2",      
        clustering_distance_columns = "euclidean", 
        clustering_method_columns = "ward.D2",     
        heatmap_legend_param = list(
          title = "Z-Score",
          legend_height = unit(4, "cm") 
        ),
        row_names_gp = gpar(fontsize = 12, face = "bold"),    
        column_names_gp = gpar(fontsize = 5)  
)
