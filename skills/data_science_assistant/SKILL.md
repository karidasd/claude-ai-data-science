---
name: data-science-assistant
description: Guides the agent during data exploration, data cleaning, statistical analysis, model building, and plotting. Triggered when working on python data science scripts, CSV files, pandas, numpy, scikit-learn, and matplotlib.
---

# Data Science Assistant Skill

This skill guides you (the AI agent) in conducting high-quality, professional data science workflows on behalf of the user.

## 🛠️ Trigger Guidelines
Activate these behaviors when the user asks you to:
1. Load, clean, or analyze a tabular dataset (CSV, JSON, Parquet).
2. Write Python code using `pandas`, `numpy`, `scikit-learn`, `matplotlib`, or `seaborn`.
3. Create machine learning pipelines (train-test split, feature engineering, modeling, evaluation).
4. Perform Exploratory Data Analysis (EDA) or summarize statistical features.

---

## 📈 Analysis & Coding Best Practices

### 1. Data Loading & Inspection
- **Always inspect first**: When asked to work with a new CSV, check column names, row counts, null counts, and column types.
- **Memory efficiency**: If a dataset is large (>100MB), do not load it completely. Use `pd.read_csv(..., nrows=100)` for inspection or load it in chunks.

### 2. Exploratory Data Analysis (EDA)
- **Check Distributions**: Review summary statistics (`describe()`) and value counts for categorical fields.
- **Handle Missing Values**: Document how you treat nulls (imputation, dropping) and provide a rationale.
- **Correlations**: Look for correlation matrices before doing predictive modeling to detect collinearity.

### 3. Data Visualization
- **Plot Quality**: Always set titles, X/Y labels, legends, and grid lines.
- **Styles**: Use a clean, modern color palette (e.g., `plt.style.use('seaborn-v0_8-whitegrid')` if available, or clean custom hex codes).
- **Output**: Save plots in high resolution (`dpi=150` or `dpi=300`) as PNG/PDF.

### 4. Machine Learning & Modeling
- **Data Leakage**: Ensure train-test split occurs *before* any feature scaling or imputation (e.g. using `sklearn.model_selection.train_test_split`).
- **Target Imbalance**: Check if the target column is imbalanced. If yes, suggest techniques (SMOTE, class weights, stratified splitting) and use precision/recall/F1 metrics instead of raw accuracy.
- **Model Evaluation**: Provide a clear evaluation report (Confusion Matrix, ROC-AUC, classification report) and plot feature importances.

---

## 📋 Suggested Conversation Flow
1. **Understand & Define**: Ask the user what their target variable is and what business question they want to answer.
2. **Explore**: Summarize the dataset shape and variables.
3. **Formulate Plan**: List the preprocessing, modeling, and evaluation steps.
4. **Implement & Deliver**: Write clean, modular, and self-documenting python code using `# %%` interactive cells.
