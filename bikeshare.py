import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
DAYS = {'ALL','SATURDAY', 'SUNDAY','MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY'}
MONTHS = {'ALL','JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER'}
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
    
    # Get the city as input, if the city is not in the list then it will ask the user again
    city = ''
    while(city not in CITY_DATA):
        city = input('Enter the city:')

    # TO DO: get user input for month (all, january, february, ... , june)
    
    # Get the month
    # Added a check to confirm if the entered month is correct , or if it is 'all'
    month = ''
    while month.upper() not in MONTHS:
        month = input('Enter the month:')
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    # Get the day
    # Added a check to confirm if the entered day is correct , or if it is 'all'
    day = ''
    while day.upper() not in DAYS:
        day = input('Enter the day:')
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
    
    # Load the CSV file based on the city input
    if city == 'chicago':
        df = pd.read_csv('./chicago.csv')
    elif city == 'new york city':
        df = pd.read_csv('./new_york_city.csv')
    elif city == 'washington':
        df = pd.read_csv('./washington.csv')

    # Filter the data by month after converting the month name to a number
    if month.upper() != 'ALL':
        datetime_object = dt.datetime.strptime(month, '%B')
        month_number = datetime_object.month
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df = df[df['Start Time'].dt.month == month_number]
        
    # Filter the data by day after converting the day name to a number
    if day.upper() != 'ALL':
        datetime_object = dt.datetime.strptime(day, '%A')
        day_number = datetime_object.day
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df = df[df['Start Time'].dt.day == day_number]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day
    # TO DO: display the most common month
    most_common_month = df['month'].mode()

    # TO DO: display the most common day of week
    most_common_day = df['day'].mode()

    # TO DO: display the most common start hour
    most_common_start_hour = df['hour'].mode()
    
    print('Most common month: ',most_common_month)
    print('Most common day: ' , most_common_day)
    print('Most common start hour: ', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()

    # TO DO: display most frequent combination of start station and end station trip
    most_common_combination = df.groupby(['Start Station','End Station']).size().idxmax()

    print('Most common start station: ' , most_common_start_station)
    print('Most common end station: ' , most_common_end_station)
    print('Most common combination: ' , most_common_combination)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['trip'] = df['End Time'] - df['Start Time']
    # TO DO: display total travel time
    total_travel_time = df['trip'].sum()

    # TO DO: display mean travel time
    mean_travel_time = df['trip'].mean()

    print('Total travel time: ' , total_travel_time)
    print('Mean travel time: ' , mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    # Function to display the rows to the user
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while view_data != 'no':
        print(df.loc[start_loc:start_loc+4 , :])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
    
    
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    counts_of_user_types = df['User Type'].value_counts()
    print('Counts of user types: ' , counts_of_user_types)
    
    # added a check for Washington
    try:
    # TO DO: Display counts of gender
        counts_of_gender = df['Gender'].value_counts()
        print('Counts of gender: ' , counts_of_gender)
    except:
        print('No data found')
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        birth_year = df['Birth Year'].dropna(axis = 0)
        earliest = int(birth_year.min())
        most_recent = int(birth_year.max())
        most_common = int(birth_year.mode())
        print('Earliest year of birth: ' , earliest)
        print('Most recent year of birth: ', most_recent)
        print('Most common year of birth: ' , most_common)
    except:
        print('no data found')
    
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
