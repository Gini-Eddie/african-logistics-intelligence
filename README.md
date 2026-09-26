# African Logistics Intelligence System

An evolving Machine Learning and Geospatial Intelligence project exploring how data, optimization and spatial intelligence can be used to improve last-mile logistics operations.

The project is being developed incrementally, beginning with a synthetic Lagos delivery operation and progressively introducing real geospatial data, road-network intelligence, optimization and Machine Learning.

## Project Objective

Last-mile logistics involves more than finding the shortest route between two locations.

A dispatcher may need to consider:

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

# Current Development

The project is currently being developed through successive engineering phases.

## Phase 1 — Operational Decision Foundation

Phase 1 creates a controlled synthetic logistics environment before introducing more complex geographic and Machine Learning components.

### Scenario

The current simulation contains:

- 1 central depot in Apapa
- 60 delivery requests distributed across Lagos
- multiple delivery areas including Apapa, Yaba, Surulere, Ikeja, Maryland, Lagos Island, Victoria Island, Lekki, Ajah and Oshodi
- package weights and size classifications
- delivery priorities
- customer delivery time windows
- service-time estimates
- driver availability and operational constraints

### Synthetic Data Generation

Rather than beginning with an external dataset that might not represent the intended logistics problem, Phase 1 generates a controlled synthetic scenario.

This makes it possible to test the system architecture and decision logic before progressively introducing real-world datasets.

### SQLite Operational Database

The generated datasets are loaded into a local SQLite database.

This provides a structured operational data layer from which the decision engine can query information such as:

- deliveries
- drivers
- depot information
- capacity constraints
- time windows
- priorities

Pandas can query the SQLite database during analysis and decision processing.

### Initial Decision Engine

The first decision engine is intentionally simple.

Its purpose is to establish the operational logic required to assign deliveries while considering constraints such as:

- driver availability
- vehicle/driver capacity
- delivery weight
- delivery windows
- priority
- service requirements

This creates a baseline that can be improved as geographic and routing intelligence are introduced.

---

# Phase 2 — GIS & Geospatial Foundation

Phase 2 introduces the spatial representation of the logistics operation.

The objective is to move from treating locations as simple latitude/longitude values to understanding how those locations exist and connect within a real road network.

## Current Progress

The synthetic delivery locations and Apapa depot generated during Phase 1 have been imported into QGIS.

The points have been mapped to their geographic positions across Lagos and visually inspected against a real-world basemap.

The original CSV spatial layers have also been converted into a GeoPackage to establish a GIS-native working dataset.

Current GeoPackage structure:

```text
lagos_logistics.gpkg
│
├── deliveries
└── depot
```

Additional spatial layers will be introduced as Phase 2 progresses.

## Phase 2 Goals

The geospatial layer will progressively introduce:

- Lagos road-network data
- coordinate reference system validation
- network connectivity
- road-distance calculations
- shortest-path analysis
- estimated travel cost
- origin-destination network matrices
- spatial data-quality validation

The resulting geographic intelligence will eventually feed back into the operational decision engine developed during Phase 1.

---

# System Evolution

The current architecture can be represented as:

```text
Synthetic Operational Data
          |
          v
     SQLite Database
          |
          v
   Decision Engine
          |
          +--------------------+
                               |
                               v
                       Geospatial Layer
                               |
                               v
                       Lagos Road Network
                               |
                               v
                    Network Distance / Cost
                               |
                               v
                    Improved Decision Engine
```

Later phases will progressively introduce optimization and Machine Learning where they provide measurable value.

---

# Planned Development

Future work includes:

### Network Intelligence

- Acquire and validate Lagos road-network data
- Represent roads as a routable network
- Snap operational locations to the network
- Calculate shortest and fastest paths
- Generate network-distance/travel-time matrices

### Route & Dispatch Optimization

- Group geographically related deliveries
- Respect vehicle capacity
- Respect driver shifts
- Respect delivery time windows
- Optimize delivery sequences
- Minimize operational travel cost

### Machine Learning

ML components will be introduced where historical or simulated operational data can support predictive decisions, including potential work on:

- ETA prediction
- delay prediction
- demand forecasting
- disruption/risk estimation

### GeoAI

Remote sensing and other geospatial datasets may later be explored where they can improve operational intelligence, including applications involving accessibility, environmental conditions or disruption analysis.

---

# Current Technology

### Programming & Data

- Python
- Pandas
- NumPy
- SQLite

### GIS

- QGIS
- GeoPackage
- OpenStreetMap basemaps/data

### Planned Geospatial Engineering

- GeoPandas
- Shapely
- OSMnx
- NetworkX

### Planned Machine Learning

- scikit-learn
- XGBoost

The planned technologies are not necessarily implemented in the current project version.

---

# Data Disclaimer

The current delivery scenario is synthetic.

Although the generated coordinates correspond to geographic positions around Lagos, they should not be interpreted as verified customer addresses or real logistics transactions.

Synthetic data is being used to develop and test the system architecture before progressively introducing suitable real-world datasets.

Open geographic datasets used in later stages will also be evaluated for completeness, accuracy and operational limitations rather than being treated automatically as ground truth.

---

# Project Philosophy

This project is being developed around a simple principle:

**Build first, learn what the build requires, and progressively increase the intelligence of the system.**

The objective is not to add Machine Learning to every component.

Instead, each layer should solve a specific operational problem:

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

The project therefore serves both as an engineering case study and as an exploration of the intersection between Machine Learning, geospatial systems and real-world logistics operations.

---

## Author

**Ginikachukwu Edward**

ML Engineer | Building intelligent systems for real-world business impact.