import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import StratifiedKFold, train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
)
import matplotlib.pyplot as plt
from umap import UMAP

# Load training data
train_file_path = "C:/Pakwithreplicate/MLproteinPakistani02.csv"
train_data = pd.read_csv(train_file_path)

# Clean data: remove infinite and NaN values
data_clean = train_data.replace([np.inf, -np.inf], np.nan).dropna()

# Select features and target
X = data_clean.iloc[:, 1:214]
y = data_clean.iloc[:, 0]

# Print feature and target information
print("Features:", X.columns.tolist())
print("Target:", y.name)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 检查各数据集的分布
print("Training set RA count: ", np.sum(y_train == 1))
print("Training set HC count: ", np.sum(y_train == 0))
print("Test set RA count: ", np.sum(y_test == 1))
print("Test set HC count: ", np.sum(y_test == 0))

# Standardize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)

# Fit the model on the selected features of the training data
model.fit(X_train, y_train)

# Predict on the selected features of the test data
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# Calculate accuracy, precision, recall, and F1 score
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)

# Output model performance metrics
print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1 Score: ", f1)
print("AUC: ", auc)

# Use Stratified K-Fold cross-validation with shuffling
kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X_train, y_train, cv=kfold, scoring="roc_auc")

print("Cross-validation scores:", scores)
print("Average AUC:", scores.mean())
print("Standard deviation of AUC:", scores.std())

# Use UMAP to visualize the test set in 2 dimensions
umap_model = UMAP(n_components=2)  # Initialize UMAP for 2D visualization
X_umap = umap_model.fit_transform(X_test)

# Scatter plot
plt.scatter(X_umap[:, 0], X_umap[:, 1], c=y_proba, cmap="viridis", alpha=0.8, s=2)
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")
plt.colorbar(label="Probability of Class 1")
plt.show()
# Select features using SelectFromModel
base_estimator = LogisticRegression()
sfm = SelectFromModel(estimator=base_estimator, threshold="median")
sfm.fit(X_train, y_train)

# Get selected feature indices
selected_feature_indices = sfm.get_support(indices=True)

# Get feature importances (coefficients) for logistic regression
feature_importances = np.abs(model.coef_[0])

# Create DataFrame with selected features and their importances
feature_importance_df = pd.DataFrame(
    {
        "Feature": X.columns[selected_feature_indices],
        "Importance": feature_importances[selected_feature_indices],
    }
)
feature_importance_df = feature_importance_df.sort_values(
    by="Importance", ascending=False
)

# Print top 10 important features
top_10_features = feature_importance_df.head(10)
print("\nTop 10 important features:")
print(top_10_features)


# Plotting top 10 important features
plt.figure(figsize=(10, 6))
plt.barh(top_10_features["Feature"], top_10_features["Importance"], color="darkblue")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 10 Important Features")
plt.gca().invert_yaxis()
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
