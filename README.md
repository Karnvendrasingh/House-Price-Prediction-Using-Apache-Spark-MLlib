# GlobalEstate AI
## Scalable Real Estate Price Prediction Platform
### Apache Spark MLlib · PySpark · FastAPI · Next.js · Stitch UI · Advanced Animations

**INT315 – Cluster Computing Academic Project**  
**Student:** Karnvendra Singh (Registration No: 12319454)  
**School of Computer Science & Engineering, Lovely Professional University**

---

## 1. Executive Summary & Vision

**GlobalEstate AI** is a distributed real estate price prediction and market analytics platform engineered for high-throughput continuous property valuation. It demonstrates how horizontal cluster computing overcomes single-node memory bottlenecks when performing machine learning on spatial and socioeconomic census datasets.

Initially focused on the **USA California Housing** dataset (20,640 census block group observations across 8 numerical features), the system is architected around an **extensible, schema-driven multi-country registry**. This allows international datasets (e.g. UK HM Land Registry, Germany ImmoScout24) to be registered, validated, and served through separate MLlib pipelines without platform redesign.

---

## 2. Technology Stack

- **Machine Learning & Distributed Computing:** Apache Spark 3.5.3, PySpark (`pyspark.ml`), Java 8 (`jdk1.8.0_202`)
- **Backend API:** Python 3.13 / 3.11, FastAPI, Pydantic v2, Uvicorn, Scikit-Learn (dataset acquisition)
- **Frontend Architecture:** Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Recharts, Lucide Icons, Framer Motion
- **UI Design System:** Designed via Google Stitch (`Cyber-Spatial Precision Glass & Midnight Atmosphere`)

---

## 3. High-Level Architecture

```
                    ┌────────────────────────────────────────┐
                    │          Next.js Web Frontend          │
                    │   (Dashboard, Prediction, Analytics)   │
                    └───────────────────┬────────────────────┘
                                        │ HTTP / REST
                    ┌───────────────────▼────────────────────┐
                    │            FastAPI Backend             │
                    │   (Schemas, Endpoints, Background Ops) │
                    └───────┬────────────────────────┬───────┘
                            │                        │
         ┌──────────────────▼──────┐      ┌──────────▼───────────────┐
         │  Terminal Interactive   │      │  Multi-Country Registry  │
         │     CLI (main.py)       │      │  (USA, UK, Germany JSON) │
         └──────────────────┬──────┘      └──────────────────────────┘
                            │
            ┌───────────────▼────────────────────────┐
            │       Apache Spark MLlib Pipeline      │
            │  VectorAssembler -> StandardScaler     │
            │          -> LinearRegression           │
            └───────────────┬────────────────────────┘
                            │
            ┌───────────────▼────────────────────────┐
            │   Persistent Storage (models/, data/)  │
            │  - california_housing.csv (20,640 rows)│
            │  - usa_california_lr (Fitted Pipeline) │
            │  - benchmark_results.json (History)    │
            └────────────────────────────────────────┘
```

---

## 4. Apache Spark MLlib Pipeline

1. **Ingestion:** Census observations ingested into a distributed Spark DataFrame with explicit `DoubleType` schema:
   - `MedInc`: Median income in block group ($10,000s)
   - `HouseAge`: Median house age (years)
   - `AveRooms`: Average rooms per household
   - `AveBedrms`: Average bedrooms per household
   - `Population`: Block group population
   - `AveOccup`: Average household occupants
   - `Latitude`: Block centroid latitude (°N)
   - `Longitude`: Block centroid longitude (°W)
   - Target `MedHouseVal`: Median house value ($100,000s)
2. **Feature Vector Assembly:** `VectorAssembler` consolidates the 8 continuous feature columns into a dense vector `raw_features`.
3. **Feature Scaling:** `StandardScaler` standardizes features to zero mean and unit variance (`features`).
4. **Estimator:** Spark MLlib `LinearRegression` fits weights using parallelized gradient descent.
5. **Evaluation:** `RegressionEvaluator` calculates held-out test partition metrics:
   - **Root Mean Squared Error (RMSE)**
   - **Mean Absolute Error (MAE)**
   - **Coefficient of Determination (R²)**
6. **Target Valuation Conversion:**
   $$\text{Estimated Value (USD)} = \text{Predicted Value} \times \$100,000$$

---

## 5. Quickstart & Execution Guide

### Step 1: Environment & Dataset Acquisition
The dataset script reuses local cached data or downloads the official California Housing dataset directly into `backend/data/california_housing.csv`:
```bash
python backend/scripts/fetch_dataset.py
```

### Step 2: Interactive Terminal CLI
Run the interactive terminal interface:
```bash
python main.py
```
Or run direct terminal subcommands:
```bash
python main.py train      # Train Spark MLlib model
python main.py predict    # Interactive property valuation
python main.py evaluate   # Display genuine test partition metrics
python main.py explore    # Dataset summary and correlation matrix
python main.py benchmark  # Run 25%, 50%, 100% scalability experiment
python main.py info       # Cluster status and diagnostics
```

### Step 3: Start FastAPI Backend
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive API documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Step 4: Start Next.js Frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your web browser.

### Step 5: Run Automated Test Suite
```bash
python -m pytest tests/ -v
```

---

## 6. Multi-Country Extensibility Model

The platform enforces schema guardrails via `backend/config/regions/`:
- **USA (California):** `ACTIVE` — Trained and validated on California Census data.
- **United Kingdom (England & Wales):** `PLANNED_FUTURE` — HM Land Registry schema registered; prediction disabled until training data is connected.
- **Germany:** `PLANNED_FUTURE` — ImmoScout24 schema registered; prediction disabled until validated.

If a user requests predictions for an unsupported market, the platform safely responds:
```json
{
  "error": "Model not available for region 'United Kingdom'. Currently only USA California model is trained and active."
}
```

---

## 7. Recommended Screenshots for INT315 Report Submission

1. **Terminal Model Training:** Output of `python main.py train` showing train/test counts and genuine test RMSE, MAE, R².
2. **Terminal Prediction Inference:** Output of `python main.py predict` showing input prompt and calculated valuation.
3. **Terminal Scalability Benchmark:** Output of `python main.py benchmark` showing wall-clock durations across 25%, 50%, and 100% subsets.
4. **Web UI Landing & Quick Estimator:** Dashboard view with the live California Housing Valuation Engine card.
5. **Model Performance Visualizer:** Actual vs. Predicted scatter chart and learned feature coefficient bar chart.
6. **Dataset Explorer Screen:** Paginated 20,640 records browser and Pearson correlation heatmap.
7. **Scalability Lab Screen:** Stage-wise execution bar chart (Preprocessing, Training, Inference).
8. **Country Registry Screen:** Multi-country cards showing USA active status and international schemas.
9. **Spark Web UI (`:4040`):** DAG visualization, Jobs, and Stages showing parallel task execution.

