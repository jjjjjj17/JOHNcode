# svm
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
)
import matplotlib.pyplot as plt

# 读取数据
file_path = "C:/Pakwithreplicate/MLproteinPakistani03.csv"
data = pd.read_csv(file_path)

# 将特征变量 x 和目标变量 y 定义为删除了 Level 列的数据
y = data["Level"]
x = StandardScaler().fit_transform(data.drop(columns=["Level"]))

# 清理数据中的无穷大值和缺失值
data_clean = data.replace([np.inf, -np.inf], np.nan).dropna()


# 拆分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=57, stratify=y
)

# 标准化特征
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = SVC(class_weight="balanced", probability=True)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1 Score: ", f1)

# k-fold
from sklearn.model_selection import cross_val_score

# k取5
scores = cross_val_score(model, X_train, y_train, cv=5)

print("Cross-validation scores:", scores)

print("Average accuracy:", scores.mean())
print("Standard deviation of accuracy:", scores.std())
dual_coef = model.dual_coef_
support_vectors = model.support_vectors_

# 计算特征系数
feature_coefficients = np.dot(dual_coef, support_vectors)

# 创建特征名列表
feature_names = data_clean.drop(columns=["Level"]).columns.tolist()

# 创建特征系数的数据框
feature_coefficients_df = pd.DataFrame(
    {"Feature": feature_names, "Coefficient": feature_coefficients[0]}
)

# 按系数绝对值大小排序
feature_coefficients_df["Abs_Coefficient"] = feature_coefficients_df[
    "Coefficient"
].abs()
feature_coefficients_df = feature_coefficients_df.sort_values(
    by="Abs_Coefficient", ascending=False
)

# 选择前十个重要特征
top_10_features = feature_coefficients_df.head(10)

# 绘制特征分析长条图
plt.figure(figsize=(10, 6))
plt.barh(top_10_features["Feature"], top_10_features["Coefficient"], color="skyblue")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 10 Feature Importance")
plt.gca().invert_yaxis()  # 逆转 y 轴，让系数绝对值大的特征显示在顶部
plt.show()
