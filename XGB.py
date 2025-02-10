import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
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

# 从Excel或CSV文件中读取数据
file_path = "C:/Pakwithreplicate/MLproteinPakistani01_1.csv"
data = pd.read_csv(file_path)

# 根据数据中的目标变量列名称调整
X = data.drop(columns=["Level"])
y = data["Level"]

# 清理数据中的无穷大值和缺失值
X = X.replace([np.inf, -np.inf], np.nan).dropna()
y = y[X.index]

# 拆分数据集为训练集和测试集，使用 stratify 参数确保类别比例一致
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 标准化特征
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 创建和训练XGBoost模型
model_xgb = XGBClassifier(n_estimators=10)
model_xgb.fit(X_train_scaled, y_train)

# 预测测试数据
y_pred_xgb = model_xgb.predict(X_test_scaled)
y_proba_xgb = model_xgb.predict_proba(X_test_scaled)[:, 1]

# 计算评估指标
accuracy_xgb = accuracy_score(y_test, y_pred_xgb)
precision_xgb = precision_score(y_test, y_pred_xgb)
recall_xgb = recall_score(y_test, y_pred_xgb)
f1_xgb = f1_score(y_test, y_pred_xgb)
auc_xgb = roc_auc_score(y_test, y_proba_xgb)

print("XGBoost Results:")
print("Accuracy: ", accuracy_xgb)
print("Precision: ", precision_xgb)
print("Recall: ", recall_xgb)
print("F1 Score: ", f1_xgb)
print("AUC: ", auc_xgb)

# 使用5折交叉验证评估XGBoost模型
kfold = StratifiedKFold(n_splits=5, shuffle=True)
cv_scores_xgb = cross_val_score(
    model_xgb, X_train_scaled, y_train, cv=kfold, scoring="roc_auc"
)

print("\nCross-validation scores (XGBoost):", cv_scores_xgb)
print("Average AUC (XGBoost):", cv_scores_xgb.mean())
print("Standard deviation of AUC (XGBoost):", cv_scores_xgb.std())

# 获取特征重要性
feature_importance_xgb = model_xgb.feature_importances_

# 获取特征名称
feature_names_xgb = X.columns

# 按照特征重要性从高到低排序
sorted_indices_xgb = np.argsort(feature_importance_xgb)[::-1]
top_10_feature_indices_xgb = sorted_indices_xgb[:10]
top_10_feature_names_xgb = feature_names_xgb[top_10_feature_indices_xgb]
top_10_feature_importance_xgb = feature_importance_xgb[top_10_feature_indices_xgb]

plt.figure(figsize=(10, 6))
plt.barh(top_10_feature_names_xgb, top_10_feature_importance_xgb, color="darkblue")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.gca().invert_yaxis()  # 反转 y 轴，让重要性高的特征显示在上面
plt.title("Top 10 Feature Importances")
plt.show()


# 绘制 ROC 曲线
fpr_xgb, tpr_xgb, thresholds_xgb = roc_curve(y_test, y_proba_xgb)
plt.figure(figsize=(10, 6))
plt.plot(
    fpr_xgb,
    tpr_xgb,
    color="blue",
    lw=2,
    label="ROC curve (XGBoost) (area = %0.2f)" % auc_xgb,
)
plt.plot([0, 1], [0, 1], color="gray", lw=2, linestyle="--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receiver Operating Characteristic (ROC) Curve (XGBoost)")
plt.legend(loc="lower right")
plt.show()

# 读取验证集数据
validation_file_path = "C:/Pakwithreplicate/MLproteinPakistani010.csv"
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
y_validation_pred = model_xgb.predict(X_validation_scaled)
y_validation_proba = model_xgb.predict_proba(X_validation_scaled)[:, 1]

# 计算验证集评估指标
validation_accuracy = accuracy_score(y_validation, y_validation_pred)
validation_precision = precision_score(y_validation, y_validation_pred)
validation_recall = recall_score(y_validation, y_validation_pred)
validation_f1 = f1_score(y_validation, y_validation_pred)
validation_auc = roc_auc_score(y_validation, y_validation_proba)
# 计算测试集的混淆矩阵
conf_matrix_test = confusion_matrix(y_validation, y_validation_pred)

# 打印混淆矩阵
print("Confusion Matrix on Test Data:")
print(conf_matrix_test)

# 绘制混淆矩阵
disp_test = ConfusionMatrixDisplay(confusion_matrix=conf_matrix_test)
disp_test.plot(cmap="Blues")
plt.title("Confusion Matrix on Test Data")
plt.show()

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
