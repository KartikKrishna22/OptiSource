# 🌴 OptiSource: Sustainable Palm Oil Sourcing Optimization Dashboard

---

## 📌 Overview

OptiSource is an interactive decision-support dashboard designed to optimize palm oil sourcing strategies while balancing:

- 💰 Cost efficiency  
- 🌱 Environmental sustainability  
- 🌳 Deforestation risk reduction  
- 📦 Supply reliability  

The dashboard enables users to explore precomputed optimization scenarios and visualize optimal sourcing allocations using an intuitive Streamlit interface.

This project demonstrates a real-world application of optimization, supply chain analytics, and sustainability-driven decision modeling.

---

## 🎯 Objectives

The main goals of OptiSource are:

- Optimize sourcing allocation across multiple suppliers
- Minimize environmental and deforestation impact
- Maintain supply constraints and sourcing feasibility
- Provide transparent and interactive visualization
- Enable scenario analysis for sustainability-focused sourcing

---

## 📊 Dataset

This project uses the **Indonesian Palm Oil Supply Chain Dataset**.

🔗 Kaggle Dataset:  
https://www.kaggle.com/datasets/kartikkrishna22/indonesian-palm-oil-dataset

### Dataset contains:

- Exporter profiles
- Supplier cost data
- Emissions metrics
- Deforestation risk indicators
- Trade flow and sourcing information
- Optimization-ready structured supply chain data

### Why hosted on Kaggle?

The full dataset exceeds GitHub's file size limits. Therefore:

- Full dataset → Kaggle
- Precomputed results → GitHub
- Visualization → Streamlit

This follows industry best practices.

---

## 🧠 Methodology

The optimization pipeline follows these steps:

### Step 1: Data Preparation
- Clean exporter and sourcing data
- Normalize cost and sustainability metrics
- Structure data for optimization modeling

### Step 2: Optimization Modeling
Multi-objective optimization considers:

- Cost minimization
- Emissions reduction
- Deforestation risk reduction
- Supply constraints
- Supplier allocation limits

Optimization performed offline using advanced optimization algorithms.

### Step 3: Precomputation
Optimization results are precomputed and stored as:
precomputed_results/
├── precomputed_scenarios_summary.csv
├── precomputed_detailed_results.json
├── precomputed_metadata.pkl


This ensures fast Streamlit performance.

### Step 4: Visualization Dashboard
Streamlit dashboard loads precomputed results and provides:

- Interactive scenario exploration
- Allocation visualization
- Cost vs sustainability comparison
- Downloadable sourcing results

---

## 🚀 Live Streamlit App

Access the live dashboard here:

https://optisource-8klpinioxlhsg3pkrwhtky.streamlit.app/

---

## 🖥 Features

### Interactive controls
Users can adjust:

- Required sourcing volume
- Risk weight preference
- Supplier limits
- Sustainability priorities

### Visual analytics

The dashboard provides:

- Supplier allocation charts
- Cost comparisons
- Emissions impact visualization
- Deforestation risk comparison

### Export functionality

Users can download optimized sourcing results for further analysis.

---

## 📁 Repository Structure
OptiSource/
│
├── app.py
├── requirements.txt
├── README.md
│
├── precomputed_results/
│ ├── precomputed_scenarios_summary.csv
│ ├── precomputed_detailed_results.json
│ └── precomputed_metadata.pkl
│
├── notebooks/
│ ├── model.ipynb
│ ├── model-new.ipynb
│ └── optimal_sourcing_7_model_ablation.ipynb
│
├── final_exporter_profiles.csv
└── strict_7_model_results_final.csv


---

## ⚙️ Installation (Local)

### Clone repository

```bash
git clone https://github.com/KartikKrishna22/OptiSource.git
cd OptiSource
