# Heart Disease Risk Prediction – MLOps End-to-End Project

## 📌 Project Overview

This project implements an **end-to-end MLOps pipeline** for predicting the risk of heart disease using the **UCI Heart Disease dataset**. It covers the complete ML lifecycle including data preprocessing, model training, experiment tracking, CI/CD, containerization, deployment, and monitoring.

The solution is designed to be **scalable, reproducible, and production-ready**, aligning with real-world MLOps best practices.

---

## 🎯 Problem Statement

Build a machine learning classifier to predict the **presence or absence of heart disease** based on patient health attributes, and deploy it as a **cloud-ready, monitored REST API**.

---

## Dataset Information

* **Name:** Heart Disease UCI Dataset (Cleveland)
* **Source:** UCI Machine Learning Repository
* **Features:** Age, sex, chest pain type, blood pressure, cholesterol, etc.
* **Target:** Binary classification

  * `1` → Heart disease present
  * `0` → Heart disease absent

Dataset file is located at:

```
data/heart.csv
```

---

## Repository Structure

```
heart-disease-mlops/
│
├── app/                  # FastAPI application
│   └── main.py
│
├── data/                 # Dataset
│   └── heart.csv
│
├── models/               # Trained model artifacts
│   └── heart_model.pkl
│
├── notebooks/            # EDA notebook
│   └── eda.ipynb
│
├── src/                  # Core ML code
│   ├── preprocess.py
│   ├── train.py
│   └── utils.py
│
├── tests/                # Unit tests
│   └── test_model.py
│
├── k8s/                  # Kubernetes manifests
│   ├── deployment.yaml
│   └── service.yaml
│
├── .github/workflows/    # CI/CD pipeline
│   └── mlops.yml
│
├── Dockerfile
├── requirements.txt
├── README.md
└── report.docx
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
  git clone <your-repo-url>
  cd heart-disease-mlops
```

### 2️⃣ Create Virtual Environment

```bash
  python -m venv venv

# Windows
  venv\Scripts\activate

# Linux / macOS
  source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
  pip install -r requirements.txt
```

---

## 📈 Exploratory Data Analysis (EDA)

EDA is performed in:

```
  notebooks/eda.ipynb
```

Includes:

* Data distribution analysis (histograms)
* Correlation heatmap
* Class balance visualization
* Key insights on feature relationships

---

## 🧠 Model Training & Evaluation

### Models Used

* Logistic Regression
* Random Forest Classifier

### Features

* Median imputation for missing values
* Feature scaling using `StandardScaler`
* Preprocessing handled via Scikit-learn `Pipeline`

### Metrics

* Accuracy
* Precision
* Recall
* ROC-AUC (primary selection metric)

### Train the Model

```bash
  python src/train.py
```
### CI/CD Pipeline
A GitHub Actions workflow automates linting, unit testing, model training, and artifact storage for every commit to main branch.

This will:

* Perform 5-fold cross-validation
* Track experiments using MLflow
* Select the best model based on ROC-AUC
* Save the final pipeline to `models/heart_model
