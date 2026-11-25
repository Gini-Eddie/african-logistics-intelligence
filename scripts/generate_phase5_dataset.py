
from pathlib import Path
import random

import numpy as np
import pandas as pd


# =========================================================
# PHASE 5 CONFIGURATION
# =========================================================

SEED = 42
SIMULATION_DAYS = 30

# New deliveries per day fluctuate around the target.
DAILY_DEMAND_MIN = 54
DAILY_DEMAND_MAX = 60
TARGET_DAILY_DEMAND = 58

random.seed(SEED)
np.random.seed(SEED)


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR = DATA_PROCESSED / "phase5_simulation"
DAILY_DIR = OUTPUT_DIR / "daily_schedules"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DAILY_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# LOAD EXISTING DAY 1 DATA
# =========================================================

deliveries_day1 = pd.read_csv(
    DATA_RAW / "deliveries.csv"
)

riders = pd.read_csv(
    DATA_RAW / "riders.csv"
)

depot = pd.read_csv(
    DATA_RAW / "depot.csv"
)

scenario = pd.read_csv(
    DATA_RAW / "scenario.csv"
)

required_columns = {
    "delivery_id",
    "customer_id",
    "area",
    "latitude",
    "longitude",
    "weight_kg",
    "package_size",
    "priority",
    "window_start",
    "window_end",
    "service_time_min",
}

missing = required_columns - set(deliveries_day1.columns)

if missing:
    raise ValueError(
        f"Day 1 deliveries are missing columns: {sorted(missing)}"
    )

if deliveries_day1["delivery_id"].duplicated().any():
    raise ValueError(
        "Day 1 contains duplicate delivery IDs."
    )

print("Existing Day 1 data loaded.")
print("Day 1 deliveries:", len(deliveries_day1))
print("Registered riders:", len(riders))


# =========================================================
# DELIVERY GENERATION SETTINGS
# =========================================================

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

time_windows = [
    ("09:00", "12:00"),
    ("10:00", "14:00"),
    ("12:00", "16:00"),
    ("14:00", "18:00"),
    ("09:00", "18:00"),
]

time_window_weights = [0.20, 0.20, 0.20, 0.15, 0.25]

priority_levels = ["LOW", "NORMAL", "HIGH", "URGENT"]
priority_weights = [0.10, 0.55, 0.25, 0.10]

package_sizes = ["SMALL", "MEDIUM", "LARGE"]
package_size_weights = [0.40, 0.40, 0.20]


# =========================================================
# DAILY DELIVERY GENERATOR
# =========================================================

def generate_daily_deliveries(
    day_number: int,
    number_of_deliveries: int,
) -> pd.DataFrame:
    """
    Generate entirely new deliveries for one simulated day.

    Priority escalation is deliberately excluded from this function.
    It belongs in the later daily import/preparation stage.
    """

    records = []

    for sequence in range(1, number_of_deliveries + 1):

        delivery_id = f"D{day_number:02d}{sequence:03d}"
        customer_id = f"C{day_number:02d}{sequence:03d}"

        area = random.choices(
            zone_names,
            weights=zone_weights,
            k=1,
        )[0]

        centre_lat, centre_lon = zones[area]

        latitude = centre_lat + np.random.normal(0, 0.008)
        longitude = centre_lon + np.random.normal(0, 0.008)

        package_size = random.choices(
            package_sizes,
            weights=package_size_weights,
            k=1,
        )[0]

        if package_size == "SMALL":
            weight_kg = round(random.uniform(1, 5), 1)
        elif package_size == "MEDIUM":
            weight_kg = round(random.uniform(5, 12), 1)
        else:
            weight_kg = round(random.uniform(12, 22), 1)

        priority = random.choices(
            priority_levels,
            weights=priority_weights,
            k=1,
        )[0]

        window_start, window_end = random.choices(
            time_windows,
            weights=time_window_weights,
            k=1,
        )[0]

        service_time = random.choice([5, 7, 10, 12, 15])

        records.append({
            "delivery_id": delivery_id,
            "customer_id": customer_id,
            "area": area,
            "latitude": round(latitude, 6),
            "longitude": round(longitude, 6),
            "weight_kg": weight_kg,
            "package_size": package_size,
            "priority": priority,
            "window_start": window_start,
            "window_end": window_end,
            "service_time_min": service_time,
        })

    return pd.DataFrame(records)


# =========================================================
# BUILD THE 30-DAY SCHEDULES
# =========================================================

daily_schedules = []
daily_manifest = []

# Day 1 is the existing dataset, not newly generated data.
day1 = deliveries_day1.copy()
day1["simulation_day"] = 1
day1["original_day"] = 1
day1["times_deferred"] = 0
day1["is_carryover"] = False

daily_schedules.append(day1)

daily_manifest.append({
    "simulation_day": 1,
    "schedule_type": "existing_baseline",
    "new_deliveries": len(day1),
    "source": "data/raw/deliveries.csv",
    "random_seed": SEED,
})

print("\nDay 1:")
print("Existing deliveries:", len(day1))


# Generate new delivery schedules for Days 2-30.
for day_number in range(2, SIMULATION_DAYS + 1):

    # Random demand around 58, bounded by the configured range.
    # This is new demand, not the total workload including carryovers.
    new_demand = random.randint(
        DAILY_DEMAND_MIN,
        DAILY_DEMAND_MAX,
    )

    new_deliveries = generate_daily_deliveries(
        day_number=day_number,
        number_of_deliveries=new_demand,
    )

    new_deliveries["simulation_day"] = day_number
    new_deliveries["original_day"] = day_number
    new_deliveries["times_deferred"] = 0
    new_deliveries["is_carryover"] = False

    daily_schedules.append(new_deliveries)

    daily_manifest.append({
        "simulation_day": day_number,
        "schedule_type": "synthetic_new_demand",
        "new_deliveries": len(new_deliveries),
        "source": "generated",
        "random_seed": SEED,
    })

    print(
        f"Day {day_number:02d}: "
        f"{len(new_deliveries)} new deliveries"
    )


# =========================================================
# SAVE DAILY SCHEDULES
# =========================================================

for day_number, schedule in enumerate(
    daily_schedules,
    start=1,
):
    output_path = DAILY_DIR / f"day_{day_number:02d}.csv"

    schedule.to_csv(
        output_path,
        index=False,
    )


# =========================================================
# SAVE COMBINED NEW-DEMAND DATASET
# =========================================================

all_new_demand = pd.concat(
    daily_schedules,
    ignore_index=True,
)

all_new_demand.to_csv(
    OUTPUT_DIR / "all_daily_schedules.csv",
    index=False,
)

manifest_df = pd.DataFrame(daily_manifest)

manifest_df.to_csv(
    OUTPUT_DIR / "simulation_manifest.csv",
    index=False,
)


# =========================================================
# SAVE STATIC REFERENCE DATA
# =========================================================

riders.to_csv(
    OUTPUT_DIR / "riders_reference.csv",
    index=False,
)

depot.to_csv(
    OUTPUT_DIR / "depot_reference.csv",
    index=False,
)

scenario.to_csv(
    OUTPUT_DIR / "day1_scenario_reference.csv",
    index=False,
)


# =========================================================
# SUMMARY AND VALIDATION
# =========================================================

print("\n" + "=" * 55)
print("PHASE 5 DATASET GENERATION SUMMARY")
print("=" * 55)

print("Simulation days:", SIMULATION_DAYS)
print("Day 1 existing deliveries:", len(day1))
print(
    "New deliveries, Days 2-30:",
    int(manifest_df.loc[
        manifest_df["simulation_day"] > 1,
        "new_deliveries",
    ].sum()),
)
print("Total scheduled delivery records:", len(all_new_demand))
print("Unique delivery IDs:", all_new_demand["delivery_id"].nunique())
print("Output directory:", OUTPUT_DIR)

assert len(daily_schedules) == SIMULATION_DAYS

assert all_new_demand["delivery_id"].is_unique, (
    "Delivery IDs must be unique across all generated days."
)

assert set(all_new_demand["simulation_day"]) == set(
    range(1, SIMULATION_DAYS + 1)
)

assert len(
    daily_schedules[0]
) == len(deliveries_day1), (
    "Day 1 must retain the existing delivery schedule."
)

print("\nDataset generation and validation completed.")
