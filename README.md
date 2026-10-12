# African Logistics Intelligence System

An evolving Machine Learning and Geospatial Intelligence project exploring how data, optimization and spatial intelligence can be used to improve last-mile logistics operations.

The project is being developed incrementally, beginning with a synthetic Lagos delivery operation and progressively introducing real geospatial data, road-network intelligence, optimization and Machine Learning.

---

## Project Overview

### Objective

Last-mile logistics involves more than finding the shortest route between two locations. A dispatcher may need to consider:

- Which drivers are currently available?
- How much capacity does each driver have?
- Which deliveries have strict time windows?
- Which deliveries should be prioritized?
- Which customers are geographically close?
- What routes actually connect those customers?
- How long will those routes take?
- How should deliveries be grouped among available drivers?

The objective of this project is to build an intelligent logistics system that can progressively incorporate these constraints into operational decisions.

The initial case study focuses on a simulated last-mile delivery operation in Lagos, Nigeria.

---

## Project Structure

```text
african-logistics-intelligence-start/
├── README.md                          # Project documentation
├── .gitignore                         # Git exclusion rules
├── .env.example                       # Environment template
├── pyproject.toml                     # Python project configuration
├── requirements.txt                   # Python dependencies
│
├── data/                             # Project data
│   ├── raw/                          # Raw source data (CSV files)
│   │   ├── deliveries.csv             # 60 delivery requests
│   │   ├── depot.csv                  # Central depot information
│   │   ├── riders.csv                 # 6 rider definitions
│   │   └── scenario.csv               # Scenario metadata
│   └── processed/                    # Processed/derived data
│       └── network_distance_matrix.csv  # 61×61 road-network distances
│
├── database/                         # SQLite operational database
│   └── logistics_v1.db               # Operational data (depots, riders, deliveries, scenarios)
│
├── geospatial_assets/                # Geospatial data files
│   ├── lagos_logistics.gpkg          # Original deliveries + depot (GeoPackage)
│   ├── deliveries_utm.gpkg            # Deliveries in UTM projection
│   ├── highway-utm.gpkg               # Lagos OSM road network
│   └── lagos-intelligence-qgis.qgz   # QGIS project file
│
├── notebooks/                        # Jupyter notebooks (organized by phase)
│   ├── phase2-network-analysis.ipynb    # Road network & distance matrix (Complete)
│   ├── phase3-baseline-dispatch.ipynb   # Rule-based dispatcher (Complete)
│   ├── phase4-route-optimization.ipynb   # OR-Tools VRP optimization (In Progress)
│   └── phase5-travel-time-prediction.ipynb # ML prediction (Unimplemented - Placeholder)
│
├── scripts/                          # Executable entry points
│   ├── generate_scenario.py          # Generate synthetic Lagos scenario
│   ├── create_database.py            # Load CSV data into SQLite
│   ├── baseline_dispatch.py          # Phase 1 rule-based dispatcher
│   └── network_analysis.py           # OSM network download
│
├── outputs/                          # Generated results
│   ├── phase3_baseline/              # Baseline dispatch results
│   │   └── .gitkeep
│   ├── phase4_optimization/          # VRP optimization results
│   │   └── .gitkeep
│   └── phase5_prediction/           # Prediction results (future)
│       └── .gitkeep
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── test_data_integrity.py        # Data validation tests
│   └── test_dispatch.py              # Dispatch logic tests
│
├── cache/                            # OSMnx cache (excluded from git)
│   └── *.json                        # Cached OSM network data
│
└── .venv/                            # Python virtual environment (excluded from git)
```

---

## Development Phases

### Phase 1 — Operational Decision Foundation ✅ Complete

Creates a controlled synthetic logistics environment.

**Components:**
- Synthetic Lagos scenario: 1 depot (Apapa), 60 deliveries across 10 areas, 6 riders (5 available)
- Package attributes: weights (1-22 kg), sizes (SMALL/MEDIUM/LARGE)
- Delivery constraints: priorities (URGENT/HIGH/NORMAL/LOW), time windows, service times
- Rider constraints: capacities (80-100 kg), package limits (12-15), shift schedules
- SQLite operational database for structured data storage
- Baseline dispatch engine with simple rule-based assignment

**Key Files:**
- `scripts/generate_scenario.py` — Scenario generation
- `scripts/create_database.py` — Database setup
- `scripts/baseline_dispatch.py` — Rule-based assignment logic

---

### Phase 2 — GIS & Geospatial Foundation ✅ Complete

Introduces spatial representation of the logistics operation.

**Components:**
- Geographic mapping of synthetic locations to real Lagos coordinates
- QGIS validation and visualization
- GeoPackage format for GIS-native datasets
- OpenStreetMap road network integration (Lagos)
- Road-network distance matrix calculation (61×61: depot + 60 deliveries)

**Key Files:**
- `geospatial_assets/lagos_logistics.gpkg` — Original spatial data
- `geospatial_assets/deliveries_utm.gpkg` — UTM-projected deliveries
- `geospatial_assets/highway-utm.gpkg` — Lagos road network
- `data/processed/network_distance_matrix.csv` — Shortest-path distances
- `notebooks/phase2-network-analysis.ipynb` — Geospatial pipeline
- `scripts/network_analysis.py` — Network download script

---

### Phase 3 — Baseline Dispatch with Geospatial Intelligence ✅ Complete

Integrates geospatial intelligence into the dispatch engine.

**Components:**
- Rule-based dispatch using network distances (not straight-line)
- Greedy nearest-next-stop routing
- Respects: capacity, time windows, priority, geographic clustering
- Baseline operational performance measurement

**Key Files:**
- `notebooks/phase3-baseline-dispatch.ipynb` — Dispatch with network distances
- `outputs/phase3_baseline/` — Dispatch results

---

### Phase 4 — Route Optimization with OR-Tools 🚧 In Progress

Implements optimization to improve over the baseline.

**Components:**
- Google OR-Tools constraint solver
- Capacitated Vehicle Routing Problem with Time Windows (CVRPTW)
- Uses Phase 2 network distance matrix as cost function
- Minimizes total travel distance while respecting all constraints

**Key Files:**
- `notebooks/phase4-route-optimization.ipynb` — VRP implementation
- `outputs/phase4_optimization/` — Optimization results

**Dependencies:**
- `ortools>=9.15.0`

---

### Phase 5 — Machine Learning for Travel Time Prediction ⏳ Unimplemented

Planned ML components for predictive intelligence.

**Planned Work:**
- ETA prediction models
- Delay prediction (traffic, weather, disruptions)
- Demand forecasting
- Risk estimation

**Key Files:**
- `notebooks/phase5-travel-time-prediction.ipynb` — Placeholder
- `outputs/phase5_prediction/` — Future results

---

## Quick Start

### Prerequisites

- Python 3.11+ (recommended: 3.11 or 3.12)
- Git
- Optional: QGIS (for geospatial visualization)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/african-logistics-intelligence-start.git
   cd african-logistics-intelligence-start
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment template:
   ```bash
   cp .env.example .env
   # Edit .env as needed
   ```

---

## Execution Sequence

### 1. Generate Synthetic Scenario (Phase 1)

```bash
python scripts/generate_scenario.py
```

This creates CSV files in `data/raw/`:
- `deliveries.csv` — 60 delivery requests
- `depot.csv` — Central depot
- `riders.csv` — 6 riders
- `scenario.csv` — Scenario metadata

### 2. Create SQLite Database

```bash
python scripts/create_database.py
```

Loads CSV data into `database/logistics_v1.db` for operational queries.

### 3. Download Road Network (Phase 2)

```bash
python scripts/network_analysis.py
```

Downloads Lagos road network from OpenStreetMap. Uses OSMnx with caching in `cache/`.

**Note:** The network file is large (~3.3 GB). If you already have `highway-utm.gpkg` in `geospatial_assets/`, this step is optional.

### 4. Geospatial Analysis (Phase 2)

Open and run:
```bash
jupyter notebook notebooks/phase2-network-analysis.ipynb
```

This notebook:
- Validates delivery and depot locations
- Projects coordinates to UTM
- Calculates network distances between all locations
- Saves distance matrix to `data/processed/network_distance_matrix.csv`

### 5. Baseline Dispatch (Phase 3)

Open and run:
```bash
jupyter notebook notebooks/phase3-baseline-dispatch.ipynb
```

This notebook:
- Loads deliveries, riders, and distance matrix
- Assigns deliveries using rule-based logic with network distances
- Saves results to `outputs/phase3_baseline/`

### 6. Route Optimization (Phase 4)

Open and run:
```bash
jupyter notebook notebooks/phase4-route-optimization.ipynb
```

This notebook:
- Uses OR-Tools to optimize delivery routes
- Respects capacity, time window, and other constraints
- Saves results to `outputs/phase4_optimization/`

---

## Running Tests

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_data_integrity.py

# Run with verbose output
pytest tests/ -v
```

---

## Project Architecture

```text
Synthetic Operational Data (Phase 1)
          ↓
     SQLite Database
          ↓
   Baseline Dispatch (Phase 3)
          ↓
+ GeoPackages (Phase 2)
    ↓
OSM Road Network
    ↓
Network Distance Matrix
    ↓
Optimized Routes (Phase 4)
    ↓
ML Predictions (Phase 5 - Future)
```

---

## Technology Stack

### Programming & Data
- Python 3.11+
- Pandas — Data manipulation
- NumPy — Numerical operations
- SQLite — Operational database

### GIS & Geospatial
- GeoPandas — Geospatial data handling
- Shapely — Geometry operations
- OSMnx — Street network analysis
- NetworkX — Graph algorithms
- QGIS — Geospatial visualization
- Pyogrio — Fast GeoPackage I/O

### Optimization
- Google OR-Tools — Constraint programming for VRP

### Testing
- pytest — Test framework

---

## Data Disclaimer

The current delivery scenario is **synthetic**.

Although the generated coordinates correspond to geographic positions around Lagos, they should not be interpreted as verified customer addresses or real logistics transactions.

Synthetic data is used to develop and test the system architecture before progressively introducing suitable real-world datasets.

Open geographic datasets used in later stages will be evaluated for completeness, accuracy, and operational limitations.

---

## File Tracking Notes

**Files Excluded from Git:**
- `geospatial_assets/*.gpkg` — Large GeoPackage files
- `geospatial_assets/*.qgz` — QGIS project files
- `database/*.db` — SQLite database
- `data/raw/*.csv` — Raw CSV data
- `data/processed/*.csv` — Processed data
- `cache/` — OSMnx cache
- `.venv/` — Python virtual environment
- `outputs/*` — Generated outputs (except .gitkeep files)
- `.env` — Environment files

**Files Tracked in Git:**
- Source code (`scripts/*.py`)
- Notebooks (`notebooks/*.ipynb`)
- Configuration (`.gitignore`, `requirements.txt`, `pyproject.toml`, `.env.example`)
- Tests (`tests/*.py`)
- Documentation (`README.md`)

---

## Project Philosophy

This project follows a **build-first** approach:

```text
Operational Data
    ↓
Decision Logic
    ↓
Spatial Intelligence
    ↓
Optimization
    ↓
Machine Learning
    ↓
Operational Intelligence
```

Each layer solves a specific operational problem before adding complexity. ML is introduced only where it provides measurable value over rule-based systems.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest tests/`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## License

This project is developed as a portfolio case study.

## Author

**Ginikachukwu Edward**

ML Engineer | Building intelligent systems for real-world business impact.
