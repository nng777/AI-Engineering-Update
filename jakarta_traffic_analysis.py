import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class First:
  @staticmethod
  def Data_Loading():
      df = pd.read_csv('jakarta_traffic_data.csv')
      return df

  @staticmethod
  def Data_Cleaning(df):
      df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
      numeric_cols = df.select_dtypes(include='number').columns
      for col in numeric_cols:
          df[col].fillna(df[col].mean(), inplace=True)
      df = df.round(1)

      categorical_cols = df.select_dtypes(include='object').columns
      for col in categorical_cols:
          df[col].fillna(df[col].mode()[0], inplace=True)
      df['Day_of_Week'] = df['Date'].dt.day_name()
      #df['Hour'] = df['Date'].dt.hour

      def categorize_hour(hour):
          if 7 <= hour <= 9:
              return 'Morning Rush'
          elif 10 <= hour <= 15:
              return 'Midday'
          elif 16 <= hour <= 19:
              return 'Evening Rush'
          else:
              return 'Night'
      df['Time_Period'] = df['Hour'].apply(categorize_hour)
      #df.drop(columns='Hour', inplace=True)

      return df

class Second:
  def __init__(self, df):
      self.df = df

  def peak_hour_analysis(self):
      # 1a. Hour with highest average vehicle count
      highest_vehicle_hour = self.df.groupby('Hour')['Vehicle_Count'].mean().idxmax()
      highest_vehicle_value = self.df.groupby('Hour')['Vehicle_Count'].mean().max()

      # 1b. Hour with lowest average speed
      lowest_speed_hour = self.df.groupby('Hour')['Average_Speed_kmh'].mean().idxmin()
      lowest_speed_value = self.df.groupby('Hour')['Average_Speed_kmh'].mean().min()

      print(f"Peak Hour Analysis:")
      print(
          f"- Hour with highest average vehicle count: {highest_vehicle_hour}h ({highest_vehicle_value:.0f} vehicles)")
      print(f"- Hour with lowest average speed: {lowest_speed_hour}h ({lowest_speed_value:.2f} km/h)\n")

  def location_comparison(self):
      # 2a. Average vehicle count per location
      location_avg_vehicle = self.df.groupby('Location')['Vehicle_Count'].mean()

      # 2b. Top 3 most congested locations
      top3_congested = location_avg_vehicle.sort_values(ascending=False).head(3)

      # 2c. Location with the slowest average speed
      slowest_location = self.df.groupby('Location')['Average_Speed_kmh'].mean().idxmin()
      slowest_speed = self.df.groupby('Location')['Average_Speed_kmh'].mean().min()

      print("Location Comparison:")
      print("- Top 3 most congested locations (by avg vehicle count):")
      for loc, count in top3_congested.items():
          print(f"  {loc}: {count:.0f} vehicles")

      print(f"- Location with the slowest average speed: {slowest_location} ({slowest_speed:.2f} km/h)\n")

  def weekend_vs_weekday_analysis(self):
      # Ensure 'Day_of_Week' is available
      if 'Day_of_Week' not in self.df.columns:
          self.df['Day_of_Week'] = self.df['Date'].dt.day_name()

      # Add a flag column for weekend
      self.df['Is_Weekend'] = self.df['Day_of_Week'].isin(['Saturday', 'Sunday'])

      # Group by weekend vs weekday
      weekend_data = self.df[self.df['Is_Weekend'] == True]
      weekday_data = self.df[self.df['Is_Weekend'] == False]

      avg_vehicle_weekend = weekend_data['Vehicle_Count'].mean()
      avg_vehicle_weekday = weekday_data['Vehicle_Count'].mean()

      avg_speed_weekend = weekend_data['Average_Speed_kmh'].mean()
      avg_speed_weekday = weekday_data['Average_Speed_kmh'].mean()

      print("Weekend vs Weekday Analysis:")
      print(f"- Avg vehicle count on weekends: {avg_vehicle_weekend:.0f}")
      print(f"- Avg vehicle count on weekdays: {avg_vehicle_weekday:.0f}")
      print(f"- Avg speed on weekends: {avg_speed_weekend:.2f} km/h")
      print(f"- Avg speed on weekdays: {avg_speed_weekday:.2f} km/h")

      # Optional conclusion
      if abs(avg_vehicle_weekend - avg_vehicle_weekday) > 10:
          print("→ There is a significant difference in vehicle count between weekends and weekdays.")
      else:
          print("→ Vehicle count does not differ significantly between weekends and weekdays.")

class Third:
  def __init__(self, df):
      self.df = df

  def analyze_weather_impact(self):
      # 1. Group by weather condition to get averages
      weather_stats = self.df.groupby('Weather_Condition')[['Vehicle_Count', 'Average_Speed_kmh']].mean()
      print("Average Vehicle Count and Speed by Weather Condition:")
      print(weather_stats.round(2), "\n")

      # 2. Find weather condition with lowest average speed (most severe traffic)
      slowest_condition = weather_stats['Average_Speed_kmh'].idxmin()
      slowest_speed = weather_stats['Average_Speed_kmh'].min()
      print(f"Most severe traffic occurs during: {slowest_condition} (Avg Speed: {slowest_speed:.2f} km/h)\n")

      # 3. Calculate percentage difference in avg speed between sunny and rainy
      try:
          sunny_speed = weather_stats.loc['Sunny', 'Average_Speed_kmh']
          rainy_speed = weather_stats.loc['Rainy', 'Average_Speed_kmh']
          percent_diff = ((sunny_speed - rainy_speed) / sunny_speed) * 100
          print(f"Percentage difference in average speed (Sunny vs Rainy): {percent_diff:.2f}%")
      except KeyError as e:
          print(f"Missing weather condition in dataset: {e}")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

class Fourth:
  def __init__(self, df):
      self.df = df

  def analyze_road_performance(self):
      # 1. Group by road type: average vehicle count and speed
      road_stats = self.df.groupby('Road_Type')[['Vehicle_Count', 'Average_Speed_kmh']].mean()

      # Format values
      road_stats['Vehicle_Count'] = road_stats['Vehicle_Count'].round().astype(int)
      road_stats['Average_Speed_kmh'] = road_stats['Average_Speed_kmh'].round(2)

      print("Average Vehicle Count and Speed by Road Type:")
      print(road_stats, "\n")

      # 2. Road type with most traffic volume (highest avg vehicle count)
      busiest_road_type = road_stats['Vehicle_Count'].idxmax()
      busiest_volume = road_stats['Vehicle_Count'].max()
      print(f"Road type with the most traffic volume: {busiest_road_type} ({busiest_volume} vehicles)\n")

      # 3. Road type with highest average speed
      fastest_road_type = road_stats['Average_Speed_kmh'].idxmax()
      fastest_speed = road_stats['Average_Speed_kmh'].max()
      print(f"Road type with the highest average speed: {fastest_road_type} ({fastest_speed:.2f} km/h)")

class Fifth:
  def __init__(self, df):
      self.df = df

  def analyze_rush_hours(self):
      # 1. Filter only Morning Rush and Evening Rush periods
      rush_df = self.df[self.df['Time_Period'].isin(['Morning Rush', 'Evening Rush'])]

      print("Rush Hour Analysis:\n")

      # 2. For each rush period
      for period in ['Morning Rush', 'Evening Rush']:
          period_df = rush_df[rush_df['Time_Period'] == period]

          # 2a. Most congested location (highest vehicle count)
          most_congested = period_df.groupby('Location')['Vehicle_Count'].mean().idxmax()
          max_vehicle = period_df.groupby('Location')['Vehicle_Count'].mean().max()

          # 2b. Average speed during that rush period
          avg_speed = period_df['Average_Speed_kmh'].mean()

          print(f"{period}:")
          print(f"- Most congested location: {most_congested} ({round(max_vehicle)} vehicles)")
          print(f"- Average speed: {avg_speed:.2f} km/h\n")

        # 3. Compare severity: Morning vs Evening Rush average speeds
      morning_speed = rush_df[rush_df['Time_Period'] == 'Morning Rush']['Average_Speed_kmh'].mean()
      evening_speed = rush_df[rush_df['Time_Period'] == 'Evening Rush']['Average_Speed_kmh'].mean()

      if evening_speed < morning_speed:
          worse_period = "Evening Rush"
      elif morning_speed < evening_speed:
          worse_period = "Morning Rush"
      else:
          worse_period = "Both are equally congested"

      print(f"Rush Hour Severity Comparison:")
      print(f"- Morning Rush Avg Speed: {morning_speed:.2f} km/h")
      print(f"- Evening Rush Avg Speed: {evening_speed:.2f} km/h")
      print(f"→ Worse rush hour: {worse_period}\n")

      # 4. Identify day with worst evening rush traffic (lowest avg speed)
      evening_df = rush_df[rush_df['Time_Period'] == 'Evening Rush']
      if 'Day_of_Week' not in evening_df.columns:
          evening_df['Day_of_Week'] = evening_df['Date'].dt.day_name()

      worst_day = evening_df.groupby('Day_of_Week')['Average_Speed_kmh'].mean().idxmin()
      print(f"The worst evening rush hour occurs on: {worst_day}")

class Sixth:
  def __init__(self, df):
    self.df = df

  def generate_insights(self):
    print("\n=== Traffic Insights and Recommendations ===\n")

    # 1. Three key findings
    print("🔍 Three Key Findings:")
    print("1. Weekday traffic volume is significantly higher than weekend traffic (≈46% more vehicles).")
    print("2. Morning and evening rush hours show drastically different speed patterns — evening is slower.")
    print("3. Rainy weather correlates with the slowest average speeds, highlighting weather impact on congestion.\n")

    # 2. Two data-driven recommendations
    print("✅ Two Recommendations to Improve Traffic:")
    print("1. Implement dynamic signal timing or staggered work hours to reduce evening congestion.")
    print("2. Improve road surface drainage and visibility measures to maintain better flow during rainy conditions.\n")

    # 3. One surprising insight
    print("💡 One Surprising Insight:")
    print("Despite being a non-working day, some Sundays show unusually high congestion, possibly due to recreational hotspots or weekend events.\n")

class Visualization:
  def __init__(self, df):
      self.df = df

  def visualize_traffic_patterns(self):
      # 1. Create line chart of average vehicle count by hour
      hourly_avg = self.df.groupby('Hour')['Vehicle_Count'].mean()
      plt.figure(figsize=(10, 5))
      plt.plot(hourly_avg.index, hourly_avg.values, marker='o')
      plt.title("Average Vehicle Count by Hour")
      plt.xlabel("Hour of Day")
      plt.ylabel("Average Vehicle Count")
      plt.grid(True)
      plt.xticks(range(0, 24))
      plt.show()

  def correlate_weather_and_speed(self):
      # 2. Correlation between weather condition and average speed
      weather_speed = self.df.groupby('Weather_Condition')['Average_Speed_kmh'].mean()
      print("\nAverage Speed by Weather Condition:")
      print(weather_speed.round(2))

      # Optional: encode weather condition numerically for correlation
      if 'Weather_Condition' in self.df.columns:
          df_encoded = self.df.copy()
          df_encoded['Weather_Condition_Code'] = df_encoded['Weather_Condition'].astype('category').cat.codes
          correlation = df_encoded[['Weather_Condition_Code', 'Average_Speed_kmh']].corr().iloc[0,1]
          print(f"\nCorrelation coefficient between weather and speed: {correlation:.2f}")

  def find_maintenance_windows(self):
      # 3. Identify hours with lowest traffic volume
      hourly_traffic = self.df.groupby('Hour')['Vehicle_Count'].mean().round()
      low_traffic_hours = hourly_traffic.sort_values().head(3)
      print("\nRecommended Time Windows for Road Maintenance (Lowest Traffic):")
      for hour, count in low_traffic_hours.items():
          print(f"- {hour}:00 — {int(count)} vehicles")

  def optimize_traffic_lights(self):
      # 4. Recommend light timing by traffic load
      hourly_traffic = self.df.groupby('Hour')['Vehicle_Count'].mean()
      peak_hours = hourly_traffic[hourly_traffic > hourly_traffic.mean() + hourly_traffic.std()].index.tolist()
      off_peak_hours = hourly_traffic[hourly_traffic < hourly_traffic.mean()].index.tolist()

      print("\nTraffic Light Timing Recommendations:")
      print("- Increase green light duration during peak hours:", peak_hours)
      print("- Reduce cycle times during off-peak hours:", off_peak_hours)

#1st class
df_raw = First.Data_Loading()
print(df_raw)
print(df_raw.head(5))
print(df_raw.info())

null_rows = df_raw[
    df_raw[['Vehicle_Count', 'Average_Speed_kmh', 'Weather_Condition', 'Is_Weekend']].isnull().any(axis=1)
]
print(null_rows)

clean_data = First.Data_Cleaning(df_raw)
print(clean_data)

#2nd class
Second(clean_data).peak_hour_analysis()
Second(clean_data).location_comparison()
Second(clean_data).weekend_vs_weekday_analysis()

#3rd class
Third(clean_data).analyze_weather_impact()

#4th class
Fourth(clean_data).analyze_road_performance()

#5th class
Fifth(clean_data).analyze_rush_hours()

#6th class
Sixth(clean_data).generate_insights()

#7th class
Visualization(clean_data).visualize_traffic_patterns()
Visualization(clean_data).correlate_weather_and_speed()
Visualization(clean_data).find_maintenance_windows()
Visualization(clean_data).optimize_traffic_lights()
