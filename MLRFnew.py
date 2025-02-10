import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
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
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt

# 读取数据
file_path = "C:/Pakwithreplicate/MLproteinPakistani02_1.csv"
data = pd.read_csv(file_path)

# 定义特征变量 X 和目标变量 y
X = data.drop(columns=["Level"])
y = data["Level"]

# 清理数据中的无穷大值和缺失值
X = X.replace([np.inf, -np.inf], np.nan).dropna()
y = y[X.index]

# 替换零值为列均值
X = X.replace(0, np.nan).fillna(X.mean())

# 使用 SMOTE 进行数据平衡处理
smote = SMOTE(sampling_strategy="auto", random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# 拆分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.3, random_state=42, stratify=y_resampled
)

# 检查数据集分布
print("Training set RA count: ", np.sum(y_train == 1))
print("Training set HC count: ", np.sum(y_train == 0))
print("Test set RA count: ", np.sum(y_test == 1))
print("Test set HC count: ", np.sum(y_test == 0))

# 标准化特征
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 使用随机森林算法
model = RandomForestClassifier(n_estimators=150, random_state=42)
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
print("Random Forest Results:")
print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1 Score: ", f1)
print("AUC: ", auc)

# 使用5折交叉验证评估模型
kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X, y, cv=kfold, scoring="roc_auc")

print("Cross-validation scores:", cv_scores)
print("Average AUC:", cv_scores.mean())
print("Standard deviation of AUC:", cv_scores.std())

# 获取特征重要性
feature_importance = model.feature_importances_
feature_names = X.columns

# 按照特征重要性从高到低排序
sorted_indices = np.argsort(feature_importance)[::-1]
top_10_feature_indices = sorted_indices[:10]
top_10_feature_names = feature_names[top_10_feature_indices]
top_10_feature_importance = feature_importance[top_10_feature_indices]

# 绘制前10个特征的重要性
plt.figure(figsize=(10, 6))
plt.barh(top_10_feature_names, top_10_feature_importance, color="darkblue")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.title("Top 10 Feature Importances")
plt.gca().invert_yaxis()  # 反转 y 轴，让重要性高的特征显示在上面
plt.show()

# 绘制 ROC 曲线
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
plt.figure(figsize=(10, 6))
plt.plot(fpr, tpr, color="blue", lw=2, label="ROC curve (area = %0.2f)" % auc)
plt.plot([0, 1], [0, 1], color="gray", lw=2, linestyle="--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receiver Operating Characteristic (ROC) Curve")
plt.legend(loc="lower right")
plt.show()

# 绘制混淆矩阵
cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()
