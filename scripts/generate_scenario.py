from pathlib import Path
import random
import numpy as np
import pandas as pd


# =========================================================
# CONFIGURATION
# =========================================================

SEED = 42
NUM_DELIVERIES = 60

random.seed(SEED)
np.random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "scenario"

DATA_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# 1. DEPOT
# =========================================================

# Approximate synthetic operational point in Apapa.
# We are NOT claiming this represents a specific real warehouse.

depot = pd.DataFrame([
    {
        "depot_id": "DEP001",
        "depot_name": "Apapa Central Depot",
        "area": "Apapa",
        "latitude": 6.4483,
        "longitude": 3.3590,
        "opening_time": "07:00",
        "closing_time": "20:00"
    }
])

depot.to_csv(DATA_DIR / "depot.csv", index=False)


# =========================================================
# 2. RIDERS
# =========================================================

riders = pd.DataFrame([
    {
        "rider_id": "R001",
        "vehicle_type": "motorcycle",
        "available": True,
        "shift_start": "08:00",
        "shift_end": "18:00",
        "break_start": "13:00",
        "break_end": "14:00",
        "capacity_kg": 100,
        "max_packages": 15
    },
    {
        "rider_id": "R002",
        "vehicle_type": "motorcycle",
        "available": True,
        "shift_start": "08:00",
        "shift_end": "18:00",
        "break_start": "13:00",
        "break_end": "14:00",
        "capacity_kg": 100,
        "max_packages": 15
    },
    {
        "rider_id": "R003",
        "vehicle_type": "motorcycle",
        "available": True,
        "shift_start": "08:00",
        "shift_end": "16:00",
        "break_start": "12:00",
        "break_end": "13:00",
        "capacity_kg": 80,
        "max_packages": 12
    },
    {
        "rider_id": "R004",
        "vehicle_type": "motorcycle",
        "available": True,
        "shift_start": "10:00",
        "shift_end": "19:00",
        "break_start": "14:00",
        "break_end": "15:00",
        "capacity_kg": 100,
        "max_packages": 15
    },
    {
        "rider_id": "R005",
        "vehicle_type": "motorcycle",
        "available": True,
        "shift_start": "09:00",
        "shift_end": "18:00",
        "break_start": "13:00",
        "break_end": "14:00",
        "capacity_kg": 80,
        "max_packages": 12
    },
    {
        "rider_id": "R006",
        "vehicle_type": "motorcycle",
        "available": False,
        "shift_start": "08:00",
        "shift_end": "18:00",
        "break_start": "12:00",
        "break_end": "13:00",
        "capacity_kg": 100,
        "max_packages": 15
    }
])

riders.to_csv(DATA_DIR / "riders.csv", index=False)


# =========================================================
# 3. LAGOS DELIVERY ZONES
# =========================================================

# Approximate zone centres.
# Random customer points will be generated around these centres.

zones = {
    "Apapa": (6.4483, 3.3590),
    "Surulere": (6.4969, 3.3532),
    "Yaba": (6.5158, 3.3707),
    "Oshodi": (6.5550, 3.3433),
    "Ikeja": (6.6018, 3.3515),
    "Maryland": (6.5720, 3.3670),
    "Lagos Island": (6.4549, 3.4246),
    "Victoria Island": (6.4281, 3.4219),
    "Lekki": (6.4698, 3.5852),
    "Ajah": (6.4690, 3.5650),
}


# Distribution intentionally creates clusters.

zone_probabilities = {
    "Apapa": 0.08,
    "Surulere": 0.12,
    "Yaba": 0.10,
    "Oshodi": 0.10,
    "Ikeja": 0.15,
    "Maryland": 0.10,
    "Lagos Island": 0.08,
    "Victoria Island": 0.10,
    "Lekki": 0.10,
    "Ajah": 0.07,
}

zone_names = list(zone_probabilities.keys())
zone_weights = list(zone_probabilities.values())


# =========================================================
# DELIVERY ATTRIBUTE OPTIONS
# =========================================================

time_windows = [
    ("09:00", "12:00"),
    ("10:00", "14:00"),
    ("12:00", "16:00"),
    ("14:00", "18:00"),
    ("09:00", "18:00")
]

time_window_weights = [
    0.20,
    0.20,
    0.20,
    0.15,
    0.25
]

priority_levels = ["LOW", "NORMAL", "HIGH", "URGENT"]

priority_weights = [0.10, 0.55, 0.25, 0.10]

package_sizes = ["SMALL", "MEDIUM", "LARGE"]

package_size_weights = [0.40, 0.40, 0.20]


# =========================================================
# 4. GENERATE DELIVERIES
# =========================================================

deliveries = []

for i in range(1, NUM_DELIVERIES + 1):

    zone = random.choices(
        zone_names,
        weights=zone_weights,
        k=1
    )[0]

    centre_lat, centre_lon = zones[zone]

    # Small geographic jitter around the zone centre.
    latitude = centre_lat + np.random.normal(0, 0.008)
    longitude = centre_lon + np.random.normal(0, 0.008)

    package_size = random.choices(
        package_sizes,
        weights=package_size_weights,
        k=1
    )[0]

    # Weight depends partly on package size.
    if package_size == "SMALL":
        weight = round(random.uniform(1, 5), 1)

    elif package_size == "MEDIUM":
        weight = round(random.uniform(5, 12), 1)

    else:
        weight = round(random.uniform(12, 22), 1)

    priority = random.choices(
        priority_levels,
        weights=priority_weights,
        k=1
    )[0]

    window_start, window_end = random.choices(
        time_windows,
        weights=time_window_weights,
        k=1
    )[0]

    service_time = random.choice([5, 7, 10, 12, 15])

    deliveries.append({
        "delivery_id": f"D{i:03}",
        "customer_id": f"C{i:03}",
        "area": zone,
        "latitude": round(latitude, 6),
        "longitude": round(longitude, 6),
        "weight_kg": weight,
        "package_size": package_size,
        "priority": priority,
        "window_start": window_start,
        "window_end": window_end,
        "service_time_min": service_time
    })


deliveries_df = pd.DataFrame(deliveries)

deliveries_df.to_csv(
    DATA_DIR / "deliveries.csv",
    index=False
)


# =========================================================
# 5. SCENARIO METADATA
# =========================================================

scenario = pd.DataFrame([
    {
        "scenario_id": "LAGOS_V1_DAY001",
        "city": "Lagos",
        "country": "Nigeria",
        "registered_riders": 6,
        "planned_deliveries": NUM_DELIVERIES,
        "vehicle_type": "motorcycle",
        "depot_count": 1,
        "scenario_type": "synthetic",
        "random_seed": SEED
    }
])

scenario.to_csv(
    DATA_DIR / "scenario.csv",
    index=False
)


# =========================================================
# SUMMARY
# =========================================================

print("\nScenario generated successfully.")
print("-" * 50)

print(f"Deliveries: {len(deliveries_df)}")
print(f"Total package weight: {deliveries_df['weight_kg'].sum():.1f} kg")
print(f"Available riders: {riders['available'].sum()}")

print("\nDeliveries by area:")
print(deliveries_df["area"].value_counts())

print("\nDeliveries by time window:")
print(
    deliveries_df
    .groupby(["window_start", "window_end"])
    .size()
)

print("\nTotal weight by area:")
print(
    deliveries_df
    .groupby("area")["weight_kg"]
    .sum()
    .sort_values(ascending=False)
)