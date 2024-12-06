import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

VALID_MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
VALID_DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_user_input(prompt, valid_values):
    """Helper function to get validated user input."""
    while True:
        value = input(prompt).strip().lower()
        if value in valid_values:
            return value
        print(f"Invalid input. Please choose from {valid_values}.")

def get_filters():
    """Gets user input for city, month, and day filters."""
    print("Hello! Let's explore some US bikeshare data!")

    city = get_user_input("Which city? (chicago, new york city, washington): ", CITY_DATA.keys())
    month = get_user_input("Which month? (all, january, ..., june): ", VALID_MONTHS)
    day = get_user_input("Which day? (all, monday, ..., sunday): ", VALID_DAYS)

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """Loads and filters city data based on month and day."""
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A').str.lower()

    if month != 'all':
        month_idx = VALID_MONTHS.index(month)
        df = df[df['month'] == month_idx]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def display_most_common(df, column_name, label):
    """Displays the most common value in a column."""
    most_common_value = df[column_name].mode()[0]
    print(f"The most common {label} is: {most_common_value}")

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    display_most_common(df, 'month', 'month')
    display_most_common(df, 'day_of_week', 'day of the week')

    df['hour'] = df['Start Time'].dt.hour
    display_most_common(df, 'hour', 'start hour')

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    display_most_common(df, 'Start Station', 'start station')
    display_most_common(df, 'End Station', 'end station')

    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most frequent trip is from {most_common_trip[0]} to {most_common_trip[1]}.")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    mean_duration = df['Trip Duration'].mean()

    print(f"Total travel time: {total_duration} seconds.")
    print(f"Average travel time: {mean_duration:.2f} seconds.")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print(f"User types:\n{df['User Type'].value_counts()}")

    if 'Gender' in df.columns:
        print(f"\nGender breakdown:\n{df['Gender'].value_counts()}")
    else:
        print("\nGender data not available.")

    if 'Birth Year' in df.columns:
        print(f"\nEarliest year of birth: {int(df['Birth Year'].min())}")
        print(f"Most recent year of birth: {int(df['Birth Year'].max())}")
        print(f"Most common year of birth: {int(df['Birth Year'].mode()[0])}")
    else:
        print("\nBirth year data not available.")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def display_raw_data(df):
    """Displays raw data upon user request."""
    i = 0
    pd.set_option('display.max_columns', 200)

    while True:
        raw = input("\nWould you like to see 5 lines of raw data? Enter 'yes' or 'no': ").strip().lower()
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df.iloc[i:i+5])
            i += 5
            if i >= len(df):
                print("\nNo more data to display.")
                break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input("\nWould you like to restart? Enter 'yes' or 'no': ").strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()