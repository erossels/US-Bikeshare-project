"""
PROJECT 2: Exploring US Bikeshare Data
By Eduardo Rossel

The following script allows the user to select data from a city and than review data statistics of the particular data.
"""
import time
import pandas as pd
import numpy as np
# We will use the following to create tables in the terminal
# You must install terminaltable. Use: pip install terminaltables 
from terminaltables import AsciiTable

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
    print('First of all:')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = list(CITY_DATA.keys())
    city = input("1. Specify a city for analysis (chicago, new york city or washington): ").lower()
    
    while city not in cities:
        city = input('Are you sure?. Please select one of the following: chicago, new york city or washington. ')
    
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("2. Select a month for analysis. You can also enter 'all' if you don't want to select and specific month: ").lower()
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'november', 'december', 'all']
    while month not in months:
        month = input('Please write a valid month: january, february, ... :' )

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("3. Select a day (monday, tuesday, ...) for analysis. You can also enter 'all' if you don't want to select and specific day: ").lower()
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while day not in days:
        day = input('Please write a valid day (monday, tuesday, ...) :' )

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

    # load data file of specified city into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name().apply(lambda x: x.lower())
    df['day_of_week'] = df['Start Time'].dt.day_name().apply(lambda x: x.lower())
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n1. Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()
    print('The most common month for traveling is: {}\n'.format(most_common_month[0].title()))

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()
    print('The most common day for traveling is: {}\n'.format(most_common_day[0].title()))

    # TO DO: display the most common start hour
    most_common_start_hour = df['hour'].mode()
    print('The most common day for traveling is: {}\n'.format(most_common_start_hour[0]))

    print("\nThis took %s seconds." % "{:.2}".format(time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n2. Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_used_start_station = df['Start Station'].mode()
    print('The most commonly used start station is: {}\n'.format(most_used_start_station[0]))

    # TO DO: display most commonly used end station
    most_used_end_station = df['End Station'].mode()
    print('The most commonly used end station is: {}\n'.format(most_used_end_station[0]))     
    # TO DO: display most frequent combination of start station and end station trip
    most_frecuent_combination = (df['Start Station']+' to '+df['End Station']).mode()
    print('The most frequent combination of start station and end station trip is: {}\n'.format(most_frecuent_combination[0]))

    print("\nThis took %s seconds." % "{:.2}".format(time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n3. Calculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print("The total time of travel is : {} hours\n".format(round(total_time/3600,1)))


    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("The average time of travel is : {} minutes\n".format(round(mean_time/60,1)))


    print("\nThis took %s seconds." % "{:.2}".format(time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n4. Calculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Travel count on user types:\n')
    # We will create a table with AsciiTable to show the user stats:
    user_types = df['User Type'].fillna("Non Value").unique()
    user_counts = df['User Type'].fillna("Non Value").value_counts()
    user_table = [
    ['Type of User', 'Count', '% of total']
    ]
    row = []
    for i in range(0, len(user_types)):
        row.append(user_types[i])
        row.append(user_counts[i])
        row.append("{:.1%}".format(user_counts[i]/user_counts.sum()))
        user_table.append(row)
        row = []
    
    user_table = AsciiTable(user_table)
    print(user_table.table+"\n")


    # TO DO: Display counts of gender
    # Check if the df has Gender data, if so print a table with the data
    if 'Gender' in df.columns:
        print('Travel count on gender types:\n')
        gender_types = df['Gender'].fillna("Non Value").unique()
        gender_counts = df['Gender'].fillna("Non Value").value_counts()
        gender_table = [
            ['Gender', 'Count', '% of total']
        ]
        row = []
        for i in range(0, len(gender_types)):
            row.append(gender_types[i])
            row.append(gender_counts[i])
            row.append("{:.1%}".format(gender_counts[i]/gender_counts.sum()))
            gender_table.append(row)
            row = []
    
        gender_table = AsciiTable(gender_table)
        print(gender_table.table+"\n")
        

    # TO DO: Display earliest, most recent, and most common year of birth
    # Check if the df has Birth Year data, if so...print the data
    if 'Birth Year' in df.columns:
        min_year_birth = df['Birth Year'].min()
        max_year_birth = df['Birth Year'].max()
        mode_year_birth = df['Birth Year'].mode()

        print('Earliest year of birth: {}\n'.format(int(min_year_birth)))
        print('Most recent year of birth: {}\n'.format(int(max_year_birth)))
        print('Most common year of birth: {}\n'.format(int(mode_year_birth[0])))

    print("\nThis took %s seconds." % "{:.2}".format(time.time() - start_time))
    print('-'*40)
    
def show_data(df):
    # Ask if the user wants to see the data
    user_answer = input('\nDo you want to see the data? Type Yes/No :\n')
    while user_answer.lower() not in ['no', 'yes']:
        user_answer = input('Please submit a valid answer, type Yes or No: \n')
        
    if user_answer == 'yes':
        i, f = 0, 5
        while user_answer == 'yes':
            print(df[i:f])
            user_answer = input('Want to see more? Type Yes/No :').lower()
            i += 5
            f += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        if df.empty:
            print('No data matches your selection')
            break

        time_stats(df)
        input('Press any key to continue...')
        station_stats(df)
        input('Press any key to continue...')
        trip_duration_stats(df)
        input('Press any key to continue...')
        user_stats(df)
        input('Press any key to continue...')
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
