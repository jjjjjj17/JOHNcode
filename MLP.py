import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance
import os

# 读取数据
file_path = "C:/Pakwithreplicate/MLproteinPakistani02.csv"
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

# 训练模型
model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=1)
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

# 计算置换重要性
perm_importance = permutation_importance(
    model, X_test_scaled, y_test, n_repeats=10, random_state=42
)

# 获取特征重要性和对应的特征名称
sorted_indices = perm_importance.importances_mean.argsort()[::-1]
feature_names = X.columns[sorted_indices]
feature_importance = perm_importance.importances_mean[sorted_indices]

# 打印前15个重要特征
top_15_features = pd.DataFrame(
    {"Feature": feature_names[:20], "Importance": feature_importance[:20]}
)
print("Top 15 Important Features:")
print(top_15_features)


# 绘制特征重要性条形图
plt.figure(figsize=(10, 6))
plt.barh(top_15_features["Feature"], top_15_features["Importance"], color="darkblue")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 20 Important Features")
plt.gca().invert_yaxis()
plt.show()

# 绘制ROC曲线
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

# 绘制混淆矩阵
cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()
#######################################################################################################################
# DEP 自己k fold
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
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
file_path = "C:/Pakwithreplicate/MLproteinPakistani12.csv"
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

# 创建 MLP 模型
model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)
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

print("MLP Results:")
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
# MLP没有直接的特征重要性属性，因此使用permutation importance
from sklearn.inspection import permutation_importance

results = permutation_importance(model, X_test_scaled, y_test, scoring="roc_auc")
importances = results.importances_mean
std = results.importances_std

# 获取特征名称
feature_names = X.columns

# 按照特征重要性从高到低排序
sorted_indices = np.argsort(importances)[::-1]
top_20_feature_indices = sorted_indices[:28]
top_20_feature_names = feature_names[top_20_feature_indices]
top_20_feature_importance = importances[top_20_feature_indices]
top_20_feature_std = std[top_20_feature_indices]

# 输出到 CSV 文件
pd.DataFrame(
    {"Feature": top_20_feature_names, "Importance": top_20_feature_importance}
).to_csv("C:/China/top_15_feature4.csv", index=False)

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

####################################################################################################################
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance
import os

# 读取数据
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

# 训练模型
model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=1)
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

# 计算置换重要性
perm_importance = permutation_importance(
    model, X_test_scaled, y_test, n_repeats=10, random_state=42
)

# 获取特征重要性和对应的特征名称
sorted_indices = perm_importance.importances_mean.argsort()[::-1]
feature_names = X.columns[sorted_indices]
feature_importance = perm_importance.importances_mean[sorted_indices]

# 打印前15个重要特征
top_15_features = pd.DataFrame(
    {"Feature": feature_names[:10], "Importance": feature_importance[:10]}
)
print("Top 10 Important Features:")
print(top_15_features)
# 输出top 10的蛋白质及其重要性为CSV文件
print("\nTop 10 important features:")
print(top_15_features)


# 绘制特征重要性条形图
plt.figure(figsize=(10, 6))
plt.barh(top_15_features["Feature"], top_15_features["Importance"], color="darkblue")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 10 Important Features")
plt.gca().invert_yaxis()
plt.show()

# 绘制ROC曲线
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
#
