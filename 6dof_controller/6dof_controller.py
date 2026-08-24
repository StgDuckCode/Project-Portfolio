# activate virtual environment if needed:
# pip install --upgrade setuptools
# pip install hidapi
# pip install xarm
# pip install pandas

import time
import csv
import pandas as pd
import xarm

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
INPUT_CSV = 'servo_data.csv'          # Input CSV file with target positions
OUTPUT_CSV = 'recorded_servo_positions.csv'  # Output CSV file for recorded actual positions

# Expected column names in the input CSV
TIME_COL = 'time' # Time column, unit: milliseconds (ms)
SERVO_COLS = ['servo1', 'servo2', 'servo3', 'servo4', 'servo5', 'servo6']

# ----------------------------------------------------------------------
# Initialize the robot
# ----------------------------------------------------------------------
try:
    arm = xarm.Controller('USB')
    print("Successfully connected to xArm controller.")
except Exception as e:
    print(f"Failed to connect to xArm controller: {e}")
    exit()

# ----------------------------------------------------------------------
# Read the input CSV
# ----------------------------------------------------------------------
try:
    df = pd.read_csv(INPUT_CSV)
except FileNotFoundError:
    print(f"Error: Input file '{INPUT_CSV}' not found")
    exit()

# Ensure required columns exist
if TIME_COL not in df.columns:
    raise ValueError(f"The input CSV must contain a '{TIME_COL}' column")
for col in SERVO_COLS:
    if col not in df.columns:
        raise ValueError(f"The input CSV must contain a '{col}' column")

# Extract time (ms) and target angles for six servos
time_ms = df[TIME_COL].values
servo_angles = df[SERVO_COLS].values   # Shape: (number of rows, 6)

n_rows = len(df)

# ----------------------------------------------------------------------
# Prepare the output CSV file (write header)
# ----------------------------------------------------------------------
with open(OUTPUT_CSV, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['time_ms'] + SERVO_COLS)

# ----------------------------------------------------------------------
# Set initial positions of the servos to the first row of target angles
# ----------------------------------------------------------------------
initial_targets = servo_angles[0]
for servo_id in range(1, 7):
    # Use a generous duration (2000ms) to ensure a smooth, safe start
    arm.setPosition(servo_id, initial_targets[servo_id-1], 2000, wait=False)

# Wait for the initialization move to complete
time.sleep(4.0)

# Record the initial position with REAL timestamp
initial_real_time = time.time() * 1000  # Convert to milliseconds
start_time = initial_real_time           # Store the start time for elapsed calculations

initial_positions = []
for servo_id in range(1, 7):
    pos = arm.getPosition(servo_id, degrees=True)
    initial_positions.append(pos)

# Record the initial position with both timestamps
with open(OUTPUT_CSV, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([time_ms[0], initial_real_time, 0] + initial_positions)

print(f" Initial position recorded at command t = {time_ms[0]} ms")
print(f"   Real wall-clock time: {initial_real_time:.2f} ms")
print(f"   Actual positions: {initial_positions}")

# ----------------------------------------------------------------------
# 5. EXECUTE THE TRAJECTORY USING BACKWARD DIFFERENCE
# ----------------------------------------------------------------------
print(" Starting trajectory playback...")

for i in range(1, n_rows):
    # Current target positions for this time step
    targets = servo_angles[i]
    
    # Calculate the duration to move from the PREVIOUS waypoint to the CURRENT one
    duration_ms = time_ms[i] - time_ms[i-1]
    
    # Safety check: Prevent zero or negative duration
    if duration_ms <= 0:
        print(f"⚠️ Warning: Zero/negative duration ({duration_ms}ms) at row {i}. Forcing to 1ms.")
        duration_ms = 1

    # ------------------------------------------------------------------
    # Move all six servos SIMULTANEOUSLY to the new target
    # ------------------------------------------------------------------
    for servo_id in range(1, 7):
        arm.setPosition(servo_id, targets[servo_id-1], duration_ms, wait=False)
    
    # Wait for the movement to complete (convert ms to seconds for time.sleep)
    time.sleep(duration_ms / 1000.0)

    # ------------------------------------------------------------------
    # Read the actual positions AND record the REAL wall-clock time
    # ------------------------------------------------------------------
    real_time_ms = time.time() * 1000  # Current wall-clock time in milliseconds
    elapsed_ms = real_time_ms - start_time  # Time elapsed since the first measurement

    actual_positions = []
    for servo_id in range(1, 7):
        pos = arm.getPosition(servo_id, degrees=True)
        actual_positions.append(pos)

    # ------------------------------------------------------------------
    # Record the data with BOTH command time and real wall-clock time
    # ------------------------------------------------------------------
    with open(OUTPUT_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([time_ms[i], elapsed_ms] + actual_positions)

    # Optional: Print progress
    #print(f"   Step {i}/{n_rows-1} | Cmd: {time_ms[i]} ms | Real: {real_time_ms:.2f} ms | Elapsed: {elapsed_ms:.2f} ms")

# ----------------------------------------------------------------------
# 6. FINISHED
# ----------------------------------------------------------------------
print(" Trajectory execution finished successfully!")
print(f" Recorded positions saved to: {OUTPUT_CSV}")