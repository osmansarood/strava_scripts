import pandas as pd
import matplotlib.pyplot as plt

# Define the CSV file path
csv_file_path = 'data/shehla_10_04_2023/activities.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Filter rows where 'Activity Type' is 'Run'
runs_df = df[df['Activity Type'] == 'Run']

# Convert 'Distance' to numerical values (from kilometers to miles)
runs_df['Distance'] = pd.to_numeric(runs_df['Distance'], errors='coerce') / 1.60934  # 1 kilometer = 0.621371 miles

# Extract the year and month from 'Activity Date' and store them in new columns 'Year' and 'Month'
runs_df['Year'] = pd.to_datetime(runs_df['Activity Date']).dt.year
runs_df['Month'] = pd.to_datetime(runs_df['Activity Date']).dt.month

# Calculate the cumulative distance for all runs
cumulative_distance = []
cumulative_miles = 0

# Generate a list of months from January 2020 to October 2023
all_months = pd.date_range(start='2020-01-01', end='2023-10-01', freq='M')

for date in all_months:
    year, month = date.year, date.month
    mask = (runs_df['Year'] == year) & (runs_df['Month'] == month)
    monthly_distance = runs_df[mask]['Distance'].sum()
    cumulative_miles += monthly_distance
    cumulative_distance.append(cumulative_miles)

# Create a DataFrame to store cumulative distance per month
cumulative_df = pd.DataFrame({'Date': all_months, 'Cumulative Distance (Miles)': cumulative_distance})

# Plot the cumulative distance
plt.figure(figsize=(12, 6))
plt.plot(cumulative_df['Date'], cumulative_df['Cumulative Distance (Miles)'], marker='o', linestyle='-')
plt.title('Cumulative Distance (Miles) Over Time')
plt.xlabel('Date')
plt.ylabel('Cumulative Distance (Miles)')
plt.xticks(rotation=45)
plt.grid(True)

# Show the plot
plt.show()

