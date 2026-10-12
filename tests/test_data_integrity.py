"""
Test data integrity for the African Logistics Intelligence System.

These tests verify that the core data files are present, well-formed,
and contain the expected data.
"""

from pathlib import Path
import pandas as pd
import sqlite3


# =========================================================
# Project Configuration
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"
DATABASE_DIR = BASE_DIR / "database"


# =========================================================
# Test CSV Data Files
# =========================================================


def test_deliveries_csv_exists():
    """Test that deliveries.csv exists and is readable."""
    file_path = DATA_RAW / "deliveries.csv"
    assert file_path.exists(), f"File not found: {file_path}"
    df = pd.read_csv(file_path)
    assert len(df) > 0, "Deliveries CSV is empty"
    assert len(df) == 60, f"Expected 60 deliveries, got {len(df)}"


def test_deliveries_csv_columns():
    """Test that deliveries.csv has expected columns."""
    file_path = DATA_RAW / "deliveries.csv"
    df = pd.read_csv(file_path)
    expected_columns = [
        "delivery_id", "customer_id", "area", "latitude", "longitude",
        "weight_kg", "package_size", "priority", "window_start", 
        "window_end", "service_time_min"
    ]
    for col in expected_columns:
        assert col in df.columns, f"Missing column: {col}"


def test_riders_csv_exists():
    """Test that riders.csv exists and is readable."""
    file_path = DATA_RAW / "riders.csv"
    assert file_path.exists(), f"File not found: {file_path}"
    df = pd.read_csv(file_path)
    assert len(df) > 0, "Riders CSV is empty"
    assert len(df) == 6, f"Expected 6 riders, got {len(df)}"


def test_riders_csv_columns():
    """Test that riders.csv has expected columns."""
    file_path = DATA_RAW / "riders.csv"
    df = pd.read_csv(file_path)
    expected_columns = [
        "rider_id", "vehicle_type", "available",
        "shift_start", "shift_end", "break_start", "break_end",
        "capacity_kg", "max_packages"
    ]
    for col in expected_columns:
        assert col in df.columns, f"Missing column: {col}"


def test_depot_csv_exists():
    """Test that depot.csv exists and is readable."""
    file_path = DATA_RAW / "depot.csv"
    assert file_path.exists(), f"File not found: {file_path}"
    df = pd.read_csv(file_path)
    assert len(df) == 1, f"Expected 1 depot, got {len(df)}"


def test_scenario_csv_exists():
    """Test that scenario.csv exists and is readable."""
    file_path = DATA_RAW / "scenario.csv"
    assert file_path.exists(), f"File not found: {file_path}"
    df = pd.read_csv(file_path)
    assert len(df) > 0, "Scenario CSV is empty"


def test_network_distance_matrix_exists():
    """Test that network_distance_matrix.csv exists and is readable."""
    file_path = DATA_PROCESSED / "network_distance_matrix.csv"
    assert file_path.exists(), f"File not found: {file_path}"
    df = pd.read_csv(file_path, index_col=0)
    assert len(df) > 0, "Network distance matrix is empty"
    assert df.shape[0] == df.shape[1], "Distance matrix must be square"


def test_network_distance_matrix_values():
    """Test that network distance matrix has valid values."""
    file_path = DATA_PROCESSED / "network_distance_matrix.csv"
    df = pd.read_csv(file_path, index_col=0)
    
    # Check that diagonal is zero
    for idx in df.index:
        assert df.loc[idx, idx] == 0, f"Diagonal value at {idx} should be 0"
    
    # Check that all values are non-negative
    assert (df.values >= 0).all(), "Distance matrix contains negative values"
    
    # Check that all values are finite
    assert pd.notna(df.values).all(), "Distance matrix contains NaN values"


# =========================================================
# Test SQLite Database
# =========================================================


def test_database_exists():
    """Test that SQLite database exists."""
    db_path = DATABASE_DIR / "logistics_v1.db"
    assert db_path.exists(), f"Database not found: {db_path}"


def test_database_tables():
    """Test that SQLite database has expected tables."""
    db_path = DATABASE_DIR / "logistics_v1.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    expected_tables = ["depots", "riders", "deliveries", "scenarios"]
    for table in expected_tables:
        assert table in tables, f"Missing table: {table}"
    
    connection.close()


def test_database_deliveries_count():
    """Test that database has correct number of deliveries."""
    db_path = DATABASE_DIR / "logistics_v1.db"
    connection = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM deliveries", connection)
    assert len(df) == 60, f"Expected 60 deliveries in database, got {len(df)}"
    connection.close()


def test_database_riders_count():
    """Test that database has correct number of riders."""
    db_path = DATABASE_DIR / "logistics_v1.db"
    connection = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM riders", connection)
    assert len(df) == 6, f"Expected 6 riders in database, got {len(df)}"
    connection.close()


# =========================================================
# Test Data Consistency
# =========================================================


def test_delivery_weights_positive():
    """Test that all delivery weights are positive."""
    file_path = DATA_RAW / "deliveries.csv"
    df = pd.read_csv(file_path)
    assert (df["weight_kg"] > 0).all(), "All delivery weights should be positive"


def test_package_sizes_valid():
    """Test that all package sizes are valid."""
    file_path = DATA_RAW / "deliveries.csv"
    df = pd.read_csv(file_path)
    valid_sizes = ["SMALL", "MEDIUM", "LARGE"]
    for size in df["package_size"]:
        assert size in valid_sizes, f"Invalid package size: {size}"


def test_priorities_valid():
    """Test that all priorities are valid."""
    file_path = DATA_RAW / "deliveries.csv"
    df = pd.read_csv(file_path)
    valid_priorities = ["LOW", "NORMAL", "HIGH", "URGENT"]
    for priority in df["priority"]:
        assert priority in valid_priorities, f"Invalid priority: {priority}"


def test_time_windows_format():
    """Test that time windows are in correct format."""
    file_path = DATA_RAW / "deliveries.csv"
    df = pd.read_csv(file_path)
    
    for start, end in zip(df["window_start"], df["window_end"]):
        # Check format HH:MM
        assert ":" in start and len(start) == 5, f"Invalid start time format: {start}"
        assert ":" in end and len(end) == 5, f"Invalid end time format: {end}"
        
        # Check that end is after start
        start_h, start_m = map(int, start.split(":"))
        end_h, end_m = map(int, end.split(":"))
        start_min = start_h * 60 + start_m
        end_min = end_h * 60 + end_m
        assert end_min > start_min, f"End time {end} must be after start time {start}"
