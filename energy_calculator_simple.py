import pandas as pd

# Load the dataset
file_path = './coding_practice_python_battery_dispatch_dataset.csv'
data = pd.read_csv(file_path)

# Filter data for the date 2024-04-01
data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%d/%m/%Y %H:%M')
data_filtered = data[data['Timestamp'].dt.date == pd.to_datetime('2024-04-01', format='%Y-%m-%d').date()]

# Initialize variables for total revenue and cost
total_revenue = 0.0
total_cost = 0.0

# Calculate revenue/cost for each interval
for i in range(len(data_filtered) - 1):
    row = data_filtered.iloc[i]
    next_row = data_filtered.iloc[i + 1]

    INITIALMW = row['INITIALMW']
    TARGETMW = row['TARGETMW']
    RRP = row['RRP']

    # If the next period's INITIALMW is not available, use the TARGETMW of the current period
    if pd.isna(next_row['INITIALMW']):
        next_initialMW = row['TARGETMW']
    else:
        next_initialMW = next_row['INITIALMW']

    # Calculate the energy dispatched using linear ramping assumption
    energy_dispatched = (INITIALMW + TARGETMW) / 2 * (5 / 60)

    # Determine if the battery is charging or discharging and calculate revenue or cost accordingly
    if INITIALMW >= 0:
        total_revenue += energy_dispatched * RRP
    else:
        total_cost += abs(energy_dispatched * RRP)

print(total_revenue)
# Calculate net revenue
net_revenue = total_revenue - total_cost

print(f"Net Energy Revenue for 2024-04-01: ${net_revenue:.2f}")
