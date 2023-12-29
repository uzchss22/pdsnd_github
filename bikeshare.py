import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """Ask user to specify city(ies) and filters, month(s) and weekday(s).

    Returns:
        (str) city - name of the city(ies) to analyze
        (str) month - name of the month(s) to filter
        (str) day - name of the day(s) of week to filter
    """
    print('Hello! Let\'s explore the bike share data in the United States!')

    us_months = ['all', 'january', 'february', 'march', 'april', 'may',
                 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    cities = ['chicago', 'new york city', 'washington']

    us_days_of_week = ['all', 'monday', 'tuesday',
                       'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        city = input(f"Please select a city from {cities}: ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Please enter a valid city.")

    while True:
        month = input(f"Select a month for analysis from {us_months}: ").lower()
        if month in us_months:
            break
        else:
            print("Please enter a valid month.")

    while True:
        day = input(f"Select a day for analysis from {us_days_of_week}: ").lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print("Please enter a valid day.")

    print('-' * 40)
    return CITY_DATA[city], month, day


def load_data(city, month, day):

    df = pd.read_csv(f'./csv/{city}', encoding='cp949')
    return df


def time_stats(df):
    print('\nCalculating the most frequent travel times...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['Month'] = df['Start Time'].dt.month
    common_month = df['Month'].mode()[0]
    print(f"The most common month is: {common_month}.")

    df['Day of Week'] = df['Start Time'].dt.day_name()
    common_day = df['Day of Week'].mode()[0]
    print(f"The most common day of the week is: {common_day}.")

    df['Start Hour'] = df['Start Time'].dt.hour
    common_hour = df['Start Hour'].mode()[0]
    print(f"The most common start hour is: {common_hour}.")

    print("\nThis operation took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""
    print('\nCalculating the most popular stations and trips...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {common_start_station}")

    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {common_end_station}")

    df['Station Combination'] = df['Start Station'] + \
                                " to " + df['End Station']
    common_station_combination = df['Station Combination'].mode()[0]
    print(f"The most frequent combination of start and end stations is: {common_station_combination}")

    print("\nThis operation took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""
    print('\nCalculating trip duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time is: {total_travel_time} seconds")

    average_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time is: {round(average_travel_time, 2)} seconds")

    print("\nThis operation took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Display statistics on bikeshare users."""
    print('\nCalculating user statistics...\n')
    start_time = time.time()

 # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"Subscriber: {user_types['Subscriber']}, Customer: {user_types['Customer']}")

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f'Male: {gender_counts["Male"]}, Female: {gender_counts["Female"]}')
    else:
        print("\nGender information is not available in this dataset.")

    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print(f"\nEarliest birth year is: {int(earliest_year)}")
        print(f"Most recent birth year is: {int(most_recent_year)}")
        print(f"Most common birth year is: {int(most_common_year)}")
    else:
        print("\nBirth year information is not available in this dataset.")

    print("\nThis operation took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """Display raw data in chunks of 5 rows based on user input."""

    start_loc = 0
    while True:
        raw_data_display = input('\nWould you like to see 5 lines of raw data? Enter yes or no. : ')
        if raw_data_display.lower() != 'yes':
            break
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Please enter "yes" or "no". : ')

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
