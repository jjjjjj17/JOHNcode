import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
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

file_path = "C:/Pakwithreplicate/MLproteinPakistani01.csv"
data = pd.read_csv(file_path)

X = data.drop(columns=["Level"])
y = data["Level"]

X = X.replace([np.inf, -np.inf], np.nan).dropna()
y = y[X.index]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print("Training set RA count: ", np.sum(y_train == 1))
print("Training set HC count: ", np.sum(y_train == 0))
print("Test set RA count: ", np.sum(y_test == 1))
print("Test set HC count: ", np.sum(y_test == 0))

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(
    n_estimators=200,
    max_features="sqrt",
    class_weight="balanced",
)

model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)

print("Random Forest Results:")
print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1 Score: ", f1)
print("AUC: ", auc)

kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=17)
cv_scores_xgb = cross_val_score(
    model, X_train_scaled, y_train, cv=kfold, scoring="roc_auc"
)

print("\nCross-validation scores :", cv_scores_xgb)
print("Average AUC :", cv_scores_xgb.mean())
print("Standard deviation of AUC :", cv_scores_xgb.std())


conf_matrix_test = confusion_matrix(y_test, y_pred)

print("Confusion Matrix on Test Data:")
print(conf_matrix_test)

disp_test = ConfusionMatrixDisplay(confusion_matrix=conf_matrix_test)
disp_test.plot(cmap="Blues")
plt.title("Confusion Matrix on Test Data")
plt.show()

feature_importance = model.feature_importances_

feature_names = X.columns

sorted_indices = np.argsort(feature_importance)[::-1]
top_20_feature_indices = sorted_indices[:28]
top_20_feature_names = feature_names[top_20_feature_indices]
top_20_feature_importance = feature_importance[top_20_feature_indices]


plt.figure(figsize=(10, 6))
plt.barh(top_20_feature_names, top_20_feature_importance, color="darkblue")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.gca().invert_yaxis()
plt.title("Top 20 Feature Importances")
plt.show()

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
#########################################################################################################
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
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

file_path = "C:/Pakwithreplicate/MLproteinPakistani12.csv"
data = pd.read_csv(file_path)

X = data.drop(columns=["Level"])
y = data["Level"]

X = X.replace([np.inf, -np.inf], np.nan).dropna()
y = y[X.index]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print("Training set RA count: ", np.sum(y_train == 1))
print("Training set HC count: ", np.sum(y_train == 0))
print("Test set RA count: ", np.sum(y_test == 1))
print("Test set HC count: ", np.sum(y_test == 0))

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(
    n_estimators=200,
    max_features="sqrt",
    class_weight="balanced",
)

model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)

print("Random Forest Results:")
print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1 Score: ", f1)
print("AUC: ", auc)

conf_matrix_test = confusion_matrix(y_test, y_pred)

print("Confusion Matrix on Test Data:")
print(conf_matrix_test)

disp_test = ConfusionMatrixDisplay(confusion_matrix=conf_matrix_test)
disp_test.plot(cmap="Blues")
plt.title("Confusion Matrix on Test Data")
plt.show()

feature_importance = model.feature_importances_

feature_names = X.columns

feature_importance_df = pd.DataFrame(
    {"Feature": feature_names, "Importance": feature_importance}
)

feature_importance_df = feature_importance_df.sort_values(
    by="Importance", ascending=False
)

print("\nAll features sorted by importance:")
print(feature_importance_df)

output_path = "C:/China/top_15_feature1.csv"
feature_importance_df.head(20).to_csv(output_path, index=False)
print(f"Feature importances saved to {output_path}")

top_15_feature_df = feature_importance_df.head(20)
plt.figure(figsize=(10, 6))
plt.barh(
    top_15_feature_df["Feature"], top_15_feature_df["Importance"], color="darkblue"
)
plt.xlabel("Importance")
plt.ylabel("Features")
plt.gca().invert_yaxis()
plt.title("Top 20 Feature Importances")
plt.show()

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
