

# 📊 Predicting Financial Inclusion Using Machine Learning

## 📌 Project Overview

This project applies machine learning techniques to predict financial inclusion using socioeconomic data. Financial inclusion refers to the ability of individuals to access and use formal financial services such as banking, credit, and insurance.

Despite the growth of digital financial systems, many individuals remain financially excluded. In this study, predictive models are used to identify patterns and factors associated with financial inclusion, with the goal of supporting data-driven decision-making.

---

## 🎯 Objectives

* Perform data preprocessing and cleaning
* Conduct exploratory data analysis (EDA)
* Build and evaluate multiple classification models
* Compare model performance using appropriate metrics
* Identify key factors influencing financial inclusion

---

## 📂 Dataset

The dataset contains demographic and socioeconomic information, including:

* Age
* Income level
* Education level
* Employment status
* Geographic location
* Financial service usage indicators

**Target Variable:**
`financially_included` (1 = Yes, 0 = No)

---

## ⚙️ Methodology

### 🔹 Data Preprocessing

* Handling missing values (median/mode imputation)
* Encoding categorical variables (One-Hot Encoding)
* Feature scaling (StandardScaler)
* Feature selection (Variance Threshold)

---

### 🔹 Models Implemented

* Logistic Regression
* Decision Tree
* Random Forest
* XGBoost
* CatBoost
* TabM (Deep Learning Model using PyTorch)

---

### 🔹 Evaluation Metrics

* Accuracy
* Precision
* Recall
* F1-score
* ROC-AUC
* Confusion Matrix

Special attention was given to **class imbalance**, using:

* Class weighting
* Threshold tuning

---

## 📊 Results Summary

| Model                | F1 Score    | ROC-AUC    |
| -------------------- | ----------- | ---------- |
| Logistic Regression  | ~0.986      | ~0.993     |
| Random Forest        | ~0.986      | ~0.993     |
| XGBoost              | ~0.986      | ~0.993     |
| CatBoost             | **~0.986+** | **~0.994** |
| TabM (Deep Learning) | ~0.957      | ~0.982     |

* **CatBoost achieved the best overall performance**
* TabM improved significantly after tuning (recall ↑ from 0.84 → 0.95)
* Logistic Regression performed competitively, indicating structured relationships in the data

---

## 📈 Visualizations

The project includes:

* Confusion Matrix
* ROC Curve
* Precision-Recall Curve
* Feature Importance Plots
* Correlation Heatmap

---

## 🧠 Key Insights

* Financial inclusion is strongly influenced by:

  * Income level
  * Education
  * Geographic location

* Tree-based models performed best for this tabular dataset

* Deep learning required additional tuning to compete

* Handling class imbalance significantly improved minority class detection

---

## 🛠️ Tools & Technologies

* **Language:** Python
* **Libraries:** Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn
* **ML Models:** XGBoost, CatBoost
* **Deep Learning:** PyTorch
* **Environment:** Jupyter Notebook

---

## 🚀 How to Run the Project

```bash
# Clone repository
git clone https://github.com/your-username/financial-inclusion-project.git

# Navigate into project
cd financial-inclusion-project

# Install dependencies
pip install -r requirements.txt

# Run notebook
jupyter notebook
```

---

## 📁 Project Structure

```text
financial-inclusion-project/
│
├── data/                  # Dataset files
├── notebooks/            # Jupyter notebooks
├── models/               # Saved models (optional)
├── images/               # Plots and figures
├── README.md             # Project documentation
└── requirements.txt      # Dependencies
```

---

## 📌 Future Work

* Apply advanced deep learning models for tabular data
* Use larger and more diverse datasets
* Develop real-time prediction systems
* Evaluate fairness and bias in model predictions

---

## 📜 License

This project is for academic purposes.

---

## 👤 Author

**Danson Ng'ang'a Waweru**

Student.ID: [01/0126/9381]

[Emobilis]

---



