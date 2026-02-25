# OptiSource

OptiSource is an interactive optimization dashboard for **Palm Oil Sourcing** that helps users explore sustainable sourcing scenarios based on precomputed optimization results. The app provides insights into cost, emissions, deforestation impact, and supplier allocation given user-selected parameters.

---

## 🔍 Project Overview

Palm oil is a key agricultural commodity, but sourcing it sustainably is complex due to trade networks, environmental impact, and cost constraints. OptiSource allows users to:

- Explore trade-off trade scenarios between cost, emissions, and deforestation risk.
- Compare optimized sourcing plans against baseline sourcing.
- Visualize supplier allocations based on selected constraints.
- Download detailed results for further analysis.

The dashboard is built using **Streamlit** and visualizes precomputed results stored in CSV/JSON/Pickle files. :contentReference[oaicite:1]{index=1}

---

## 📁 Repository Structure
OptiSource/
│
├── app.py
├── precomputed_results/
│ ├── precomputed_scenarios_summary.csv
│ ├── precomputed_detailed_results.json
│ ├── precomputed_metadata.pkl
│ └── precomputed_supplier_allocations.parquet (optional)
├── final_exporter_profiles.csv
├── strict_7_model_results_final.csv
├── model-new.ipynb
├── model.ipynb
├── optimal_sourcing_7_model_ablation.ipynb
├── requirements.txt
├── LICENSE
└── README.md


---

## 📌 Key Components

### 🧠 Streamlit App (`app.py`)
This is the main dashboard that allows users to interactively select parameters such as:
- Volume required (tonnes)
- Sustainability risk weight
- Max share per supplier
- Minimum number of suppliers

The app then displays:
- Cost, emissions, deforestation comparisons
- Supplier allocation charts
- Detailed supplier information with export options to CSV :contentReference[oaicite:2]{index=2}

---

## 📊 Precomputed Data (`precomputed_results/`)

To ensure fast, responsive interaction, all optimization results are precomputed offline and stored in the `precomputed_results/` folder. These include:

- **precomputed_scenarios_summary.csv** – Summary of all scenarios
- **precomputed_detailed_results.json** – Detailed optimization outcomes
- **precomputed_metadata.pkl** – Metadata for results
- **precomputed_supplier_allocations.parquet** – Supplier allocation dataset (optional)

These files power the dashboards without heavy runtime computations. :contentReference[oaicite:3]{index=3}

---

## 🛠 Installation

### 💾 Clone the Repository

```bash
git clone https://github.com/KartikKrishna22/OptiSource.git
cd OptiSource
