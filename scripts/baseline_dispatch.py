from pathlib import Path
import sqlite3
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "logistics_v1.db"


# =========================================================
# LOAD DATA
# =========================================================

connection = sqlite3.connect(DATABASE_PATH)

riders = pd.read_sql_query(
    "SELECT * FROM riders WHERE available = 1",
    connection
)

deliveries = pd.read_sql_query(
    "SELECT * FROM deliveries",
    connection
)


# =========================================================
# TIME CONVERSION
# =========================================================

def time_to_minutes(time_string):

    hour, minute = map(
        int,
        time_string.split(":")
    )

    return hour * 60 + minute


for column in ["shift_start", "shift_end"]:
    riders[column + "_min"] = riders[column].apply(
        time_to_minutes
    )


for column in ["window_start", "window_end"]:
    deliveries[column + "_min"] = deliveries[column].apply(
        time_to_minutes
    )


# =========================================================
# PRIORITY ORDER
# =========================================================

priority_rank = {
    "URGENT": 0,
    "HIGH": 1,
    "NORMAL": 2,
    "LOW": 3
}

deliveries["priority_rank"] = deliveries[
    "priority"
].map(priority_rank)


# Tighter/earlier jobs first.

deliveries = deliveries.sort_values(
    by=[
        "window_end_min",
        "priority_rank"
    ]
)


# =========================================================
# TRACK RIDER LOADS
# =========================================================

rider_state = {}

for _, rider in riders.iterrows():

    rider_state[rider["rider_id"]] = {
        "weight": 0.0,
        "packages": 0,
        "areas": set()
    }


assignments = []
unassigned = []


# =========================================================
# ASSIGN DELIVERIES
# =========================================================

for _, delivery in deliveries.iterrows():

    candidates = []

    for _, rider in riders.iterrows():

        rider_id = rider["rider_id"]
        state = rider_state[rider_id]

        # -----------------------------------------
        # CAPACITY CHECK
        # -----------------------------------------

        new_weight = (
            state["weight"]
            + delivery["weight_kg"]
        )

        if new_weight > rider["capacity_kg"]:
            continue


        # -----------------------------------------
        # PACKAGE COUNT CHECK
        # -----------------------------------------

        if state["packages"] + 1 > rider["max_packages"]:
            continue


        # -----------------------------------------
        # TIME COMPATIBILITY
        # -----------------------------------------

        # Simple Phase 1 assumption:
        # rider's shift must overlap the customer's
        # delivery window.

        overlap_start = max(
            rider["shift_start_min"],
            delivery["window_start_min"]
        )

        overlap_end = min(
            rider["shift_end_min"],
            delivery["window_end_min"]
        )

        if overlap_start >= overlap_end:
            continue


        # -----------------------------------------
        # GEOGRAPHIC PREFERENCE
        # -----------------------------------------

        same_area = (
            delivery["area"]
            in state["areas"]
        )

        # Lower score = better.
        #
        # Prefer:
        # 1. Rider already serving same area.
        # 2. Rider with lower current weight.

        area_penalty = 0 if same_area else 100

        load_ratio = (
            new_weight
            / rider["capacity_kg"]
        )

        score = (
            area_penalty
            + load_ratio
        )


        candidates.append(
            (
                score,
                rider_id
            )
        )


    # =====================================================
    # SELECT BEST CANDIDATE
    # =====================================================

    if not candidates:

        unassigned.append(
            delivery["delivery_id"]
        )

        continue


    candidates.sort(
        key=lambda x: x[0]
    )

    _, selected_rider = candidates[0]

    state = rider_state[selected_rider]

    state["weight"] += delivery["weight_kg"]
    state["packages"] += 1
    state["areas"].add(
        delivery["area"]
    )


    assignments.append({
        "delivery_id": delivery["delivery_id"],
        "rider_id": selected_rider,
        "area": delivery["area"],
        "weight_kg": delivery["weight_kg"],
        "priority": delivery["priority"],
        "window_start": delivery["window_start"],
        "window_end": delivery["window_end"]
    })


# =========================================================
# RESULTS
# =========================================================

assignments_df = pd.DataFrame(assignments)


print("\nBASELINE DISPATCH RESULTS")
print("=" * 60)

print(
    f"Total deliveries: {len(deliveries)}"
)

print(
    f"Assigned: {len(assignments_df)}"
)

print(
    f"Unassigned: {len(unassigned)}"
)


print("\nRIDER SUMMARY")
print("-" * 60)

for rider_id, state in rider_state.items():

    print(
        f"{rider_id}: "
        f"{state['packages']} packages | "
        f"{state['weight']:.1f} kg | "
        f"Areas: {', '.join(state['areas'])}"
    )


print("\nUNASSIGNED DELIVERIES")
print("-" * 60)

if unassigned:

    print(unassigned)

else:

    print("None")


# =========================================================
# SAVE ASSIGNMENTS
# =========================================================

OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

assignments_df.to_csv(
    OUTPUT_DIR / "baseline_assignments.csv",
    index=False
)


assignments_df.to_sql(
    "baseline_assignments",
    connection,
    if_exists="replace",
    index=False
)


connection.close()