import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
)
import matplotlib.pyplot as plt
import os

# 从Excel或CSV文件中读取数据
file_path = "C:/Pakwithreplicate/MLproteinPakistani01.csv"
data = pd.read_csv(file_path)

# 定义特征变量 X 和目标变量 y
X = data.drop(columns=["Level"])
y = data["Level"]

# 清理数据中的无穷大值和缺失值
X = X.replace([np.inf, -np.inf], np.nan).dropna()
y = y[X.index]

# 拆分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 标准化特征
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 创建并训练AdaBoost模型
model = AdaBoostClassifier(n_estimators=150)
model.fit(X_train_scaled, y_train)

# 预测测试数据
y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

# 计算评估指标
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)

# 输出评估结果
print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1 Score: ", f1)
print("AUC: ", auc)

# 使用交叉验证评估模型
scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring="roc_auc")
print("Cross-validation scores:", scores)
print("Average AUC:", scores.mean())
print("Standard deviation of AUC:", scores.std())

# 获取特征重要性
feature_importance = model.feature_importances_

# 获取特征名称
feature_names = X.columns

# 创建一个包含特征名和重要性的 DataFrame
feature_importance_df = pd.DataFrame(
    {"Feature": feature_names, "Importance": feature_importance}
)

# 按照重要性排序
feature_importance_df = feature_importance_df.sort_values(
    by="Importance", ascending=False
)

# 打印所有蛋白质的排序和分数
print("\nAll features sorted by importance:")
print(feature_importance_df)

# 导出前 20 个特征的重要性到 CSV 文件
output_path = "C:/China/top_15_features2.csv"  # 修改路径为所需的文件名
feature_importance_df.head(20).to_csv(output_path, index=False)
print(f"Feature importances saved to {output_path}")

# 可视化前 20 个特征的重要性
plt.figure(figsize=(10, 6))
plt.barh(
    feature_importance_df["Feature"].head(20),
    feature_importance_df["Importance"].head(20),
    color="darkblue",
)
plt.xlabel("Importance")
plt.ylabel("Features")
plt.gca().invert_yaxis()  # 反转 y 轴，让重要性高的特征显示在上面
plt.title("Top 20 Feature Importances")
plt.show()

# 绘制 ROC 曲线
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
roc_auc = roc_auc_score(y_test, y_proba)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color="darkorange", lw=2, label=f"ROC curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel(
    "False Positive Rate", fontdict={"size": 12, "weight": "bold", "color": "black"}
)
plt.ylabel(
    "True Positive Rate", fontdict={"size": 12, "weight": "bold", "color": "black"}
)
plt.title(
    "Receiver Operating Characteristic (ROC) Curve",
    fontdict={"size": 12, "weight": "bold", "color": "black"},
)
plt.legend(loc="lower right", fontsize=12)
plt.show()

#######################################################################################################################
# DEP 自己k fold
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
)
import matplotlib.pyplot as plt
import os

# 从Excel或CSV文件中读取数据
file_path = "C:/Pakwithreplicate/MLproteinPakistani02_9.csv"
data = pd.read_csv(file_path)

# 定义特征变量 X 和目标变量 y
X = data.drop(columns=["Level"])
y = data["Level"]

# 清理数据中的无穷大值和缺失值
X = X.replace([np.inf, -np.inf], np.nan).dropna()
y = y[X.index]

# 拆分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 标准化特征
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 训练 AdaBoost 模型
model = AdaBoostClassifier(n_estimators=150)
model.fit(X_train_scaled, y_train)

# 预测
y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

# 计算评估指标
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)

print("AdaBoost Results:")
print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1 Score: ", f1)
print("AUC: ", auc)

# k-fold
scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring="roc_auc")
print("Cross-validation scores:", scores)
print("Average accuracy:", scores.mean())
print("Standard deviation of accuracy:", scores.std())

# 计算混淆矩阵
conf_matrix_test = confusion_matrix(y_test, y_pred)
print("Confusion Matrix on Test Data:")
print(conf_matrix_test)

# 绘制混淆矩阵
disp_test = ConfusionMatrixDisplay(confusion_matrix=conf_matrix_test)
disp_test.plot(cmap="Blues")
plt.title("Confusion Matrix on Test Data")
plt.show()

# 获取特征重要性
feature_importance = model.feature_importances_

# 获取特征名称
feature_names = X.columns

# 按照特征重要性从高到低排序
sorted_indices = np.argsort(feature_importance)[::-1]
top_20_feature_indices = sorted_indices[:28]
top_20_feature_names = feature_names[top_20_feature_indices]
top_20_feature_importance = feature_importance[top_20_feature_indices]

# 输出到 CSV 文件
pd.DataFrame(
    {"Feature": top_20_feature_names, "Importance": top_20_feature_importance}
).to_csv("C:/Chinanew/top28_feature2.csv", index=False)

# 绘制前 20 个特征的重要性
plt.figure(figsize=(10, 6))
plt.barh(top_20_feature_names, top_20_feature_importance, color="darkblue")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.gca().invert_yaxis()  # 反转 y 轴，让重要性高的特征显示在上面
plt.title("Top 20 Feature Importances")
plt.show()

# 绘制 ROC 曲线
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
roc_auc = roc_auc_score(y_test, y_proba)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color="darkorange", lw=2, label=f"ROC curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receiver Operating Characteristic (ROC) Curve")
plt.legend(loc="lower right")
plt.show()

##########################################################################################################
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
)
import matplotlib.pyplot as plt

# 从Excel或CSV文件中读取数据
file_path = "C:/Pakwithreplicate/MLproteinPakistani08.csv"
data = pd.read_csv(file_path)

# 定义特征变量 X 和目标变量 y
X = data.drop(columns=["Level"])
y = data["Level"]

# 清理数据中的无穷大值和缺失值
X = X.replace([np.inf, -np.inf], np.nan).dropna()
y = y[X.index]


# 拆分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 标准化特征
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 创建并训练AdaBoost模型
model = AdaBoostClassifier(n_estimators=150)
model.fit(X_train_scaled, y_train)

# 预测测试数据
y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

# 计算评估指标
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)

# 输出评估结果
print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1 Score: ", f1)
print("AUC: ", auc)

# 使用交叉验证评估模型
scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring="roc_auc")
print("Cross-validation scores:", scores)
print("Average AUC:", scores.mean())
print("Standard deviation of AUC:", scores.std())

# 获取特征重要性
feature_importance = model.feature_importances_

# 获取特征名称
feature_names = X.columns

# 按照特征重要性从高到低排序
sorted_indices = np.argsort(feature_importance)[::-1]
top_10_feature_indices = sorted_indices[:10]
top_10_feature_names = feature_names[top_10_feature_indices]
top_10_feature_importance = feature_importance[top_10_feature_indices]


plt.figure(figsize=(10, 6))
plt.barh(top_10_feature_names, top_10_feature_importance, color="darkblue")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.gca().invert_yaxis()  # 反转 y 轴，让重要性高的特征显示在上面
plt.title("Top 10 Feature Importances")
plt.show()


# Plot ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
roc_auc = roc_auc_score(y_test, y_proba)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color="darkorange", lw=2, label=f"ROC curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receiver Operating Characteristic (ROC) Curve")
plt.legend(loc="lower right")
plt.show()


# 读取验证集数据
validation_file_path = "C:/Pakwithreplicate/MLproteinPakistani07.csv"
validation_data = pd.read_csv(validation_file_path)

# 定义验证集的特征和目标变量
X_validation = validation_data.drop(columns=["Level"])
y_validation = validation_data["Level"]

# 数据清理
X_validation = X_validation.replace([np.inf, -np.inf], np.nan).dropna()
y_validation = y_validation[X_validation.index]

# 标准化验证集特征
X_validation_scaled = scaler.transform(X_validation)

# 预测验证集数据
y_validation_pred = model.predict(X_validation_scaled)
y_validation_proba = model.predict_proba(X_validation_scaled)[:, 1]

# 计算验证集评估指标
validation_accuracy = accuracy_score(y_validation, y_validation_pred)
validation_precision = precision_score(y_validation, y_validation_pred)
validation_recall = recall_score(y_validation, y_validation_pred)
validation_f1 = f1_score(y_validation, y_validation_pred)
validation_auc = roc_auc_score(y_validation, y_validation_proba)

print("\nRandom Forest Results on Validation Data:")
print("Accuracy: ", validation_accuracy)
print("Precision: ", validation_precision)
print("Recall: ", validation_recall)
print("F1 Score: ", validation_f1)
print("AUC: ", validation_auc)

# 绘制 ROC 曲线
fpr, tpr, thresholds = roc_curve(y_validation, y_validation_proba)
plt.figure(figsize=(10, 6))
plt.plot(
    fpr, tpr, color="blue", lw=2, label="ROC curve (area = %0.2f)" % validation_auc
)
plt.plot([0, 1], [0, 1], color="gray", lw=2, linestyle="--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receiver Operating Characteristic (ROC) Curve")
plt.legend(loc="lower right")
plt.show()
