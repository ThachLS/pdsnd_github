import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city would you like to explore? (chicago, new york city, washington): ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please choose from 'chicago', 'new york city', or 'washington'.")

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Which month? (all, january, february, ... , june): ").lower()
        if month in months:
            break
        else:
            print("Invalid month. Please choose from 'all', 'january', 'february', ..., or 'june'.")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Which day? (all, monday, tuesday, ... sunday): ").lower()
        if day in days:
            break
        else:
            print("Invalid day. Please choose from 'all', 'monday', 'tuesday', ..., or 'sunday'.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load the city data
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month and day of the week from the Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A').str.lower()
    
    # Filter by month if applicable
    if month != 'all':
        # Convert month name to number
        month = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month]
    
    # Filter by day of the week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.lower()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"The most common month is: {['january', 'february', 'march', 'april', 'may', 'june'][most_common_month - 1]}")

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"The most common day of the week is: {most_common_day.title()}")

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f"The most common start hour is: {most_common_hour}:00") 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {start_station}")

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {end_station}")

    # TO DO: display most frequent combination of start station and end station trip
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most frequent combination of start and end station trip is from {most_common_trip[0]} to {most_common_trip[1]}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time} seconds.")

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Average travel time: {mean_travel_time} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"User types:\n{user_types}")

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f"Gender breakdown:\n{gender_counts}")
    else:
        print("Gender data not available.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print(f"Earliest year of birth: {earliest_birth_year}")
        print(f"Most recent year of birth: {most_recent_birth_year}")
        print(f"Most common year of birth: {most_common_birth_year}")
    else:
        print("Birth year data not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_raw_data(df):
    """
    Displays raw data upon user request in an interactive manner.

    Args:
        df - Pandas DataFrame containing the filtered bikeshare data
    """
    i = 0
    pd.set_option('display.max_columns', 200)
    raw = input("\nWould you like to see 5 lines of raw data? Enter 'yes' or 'no': ").lower()

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df.iloc[i:i+5])  # Display 5 rows of raw data
            i += 5
            if i >= len(df):  # If no more data is available, notify the user
                print("\nNo more data to display.")
                break
            raw = input("\nWould you like to see 5 more lines of raw data? Enter 'yes' or 'no': ").lower()
        else:
            raw = input("\nInvalid input. Please enter only 'yes' or 'no': ").lower()    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Call display_raw_data to show raw data upon user request
        display_raw_data(df)

        # Proceed with computing and displaying statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
