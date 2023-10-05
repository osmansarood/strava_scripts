import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define the CSV file path
csv_file_path = 'data/shehla_10_04_2023/activities.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Filter rows where 'Activity Type' is 'Run'
runs_df = df[df['Activity Type'] == 'Run']

# Convert 'Distance' to numerical values (from kilometers to miles)
runs_df['Distance'] = pd.to_numeric(runs_df['Distance'], errors='coerce') / 1.60934  # 1 kilometer = 0.621371 miles

# Extract the year from 'Activity Date' and store it in a new column 'Year'
runs_df['Year'] = pd.to_datetime(runs_df['Activity Date']).dt.year

# Filter only the desired years specified in the list
desired_years = [2020, 2021, 2022, 2023]
runs_df = runs_df[runs_df['Year'].isin(desired_years)]

# Filter out workouts/rows where distance is less than 2 miles
runs_df = runs_df[runs_df['Distance'] >= 2.0]

# Calculate 'Pace' in min/mile by dividing 'Elapsed Time' (in seconds) by 'Distance'
runs_df['Pace'] = (runs_df['Elapsed Time'] / 60) / runs_df['Distance']

# Define the pace bins with a step size of 0.5 min/mile
pace_bins = np.arange(9.0, 16.0, 0.25)  # Adjust the range as needed

# Initialize lists to store average heart rate, count of data points per bin, and circle sizes for each year
average_heart_rate_by_year = {}
circle_sizes_by_year = {}

# Calculate the average heart rate and count of data points for each pace bin for each year
for year, group in runs_df.groupby('Year'):
    average_heart_rate = []
    circle_sizes = []
    for bin_start in pace_bins:
        bin_end = bin_start + 0.5
        bin_mask = (group['Pace'] >= bin_start) & (group['Pace'] < bin_end)
        bin_data = group[bin_mask]
        if not bin_data.empty:
            average_hr = bin_data['Average Heart Rate'].mean()
            num_points = len(bin_data)
            average_heart_rate.append(average_hr)
            circle_sizes.append(num_points)
        else:
            average_heart_rate.append(None)  # None for bins with no data
            circle_sizes.append(0)  # Zero size for bins with no data
    average_heart_rate_by_year[year] = average_heart_rate
    circle_sizes_by_year[year] = circle_sizes

# Plot the scatter plot for each year with enlarged circle sizes based on the number of data points
plt.figure(figsize=(10, 6))
for year in desired_years:
    plt.scatter(
        pace_bins,
        average_heart_rate_by_year[year],
        s=np.array(circle_sizes_by_year[year]) * 10,  # Enlarge dot sizes by a factor of 10
        label=f'Year {year}',
        alpha=0.5,
    )

plt.title('Average Heart Rate vs. Pace Binned (0.5 min/mile intervals)')
plt.xlabel('Pace (min/mile)')
plt.ylabel('Average Heart Rate (bpm)')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

