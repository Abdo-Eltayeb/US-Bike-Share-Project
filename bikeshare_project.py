import time
import pandas as pd
import numpy as np
import calendar

from pandas.core.frame import DataFrame
from pandas.core.indexes.base import Index

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_LIST = ["january", "february", "march", "april", "may", "june"]

DAYS_LIST = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello and welcome! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while city not in CITY_DATA.keys():
        
        print("\nPlease choose City from below:")
        print("\n'washington'")
        print("'chicago'")
        print("'new york city'")
        print("\nCity:")
        city = input().lower()
        
        if city not in CITY_DATA.keys():
            retry= int(3)
                
            while city not in CITY_DATA.keys() or retry >= 0 :
                print("\nPlease insert the City name exactly as shown above \nAvailable retries:{}".format(retry))
                city = input().lower()
                if retry == 1 or city in CITY_DATA:
                    break;
                retry -= 1
     
    print("\nYou have chosen '{}' as the City you want to check on.".format(city.title()))

    # get user input for month (all, january, february, ... , june)
    month = False
    while month not in MONTH_LIST and month != "all":
        
        print("\n\nPlease choose one Month from january until june or insert all")
        print("\nMonth:")
        month = input().lower()
        
        if month not in MONTH_LIST and month != "all":
            retry= int(3)
                
            while month not in MONTH_LIST or retry >= 0 :
                print("\nPlease retype the month all letters in lower case or choose all\nAvailable retries:{}".format(retry))
                month = input().lower()
                if retry == 1 or month in MONTH_LIST or month == "all":
                    break;
                retry -= 1
            
    print("\nYou have chosen '{}' as month/s".format(month.title()))
     

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = False
    while day not in DAYS_LIST and day != "all":
        print("\n\nPlease choose one day from the week or insert All")
        print("\nDay:")
        day = input().lower()
        
        if day not in DAYS_LIST and day != "all":
            retry= int(3)
                
            while day not in DAYS_LIST or retry >= 0 :
                print("\nPlease retype the day all letters in lower case or choose all\nAvailable retries:{}".format(retry))
                day = input().lower()
                if retry == 1 or day in DAYS_LIST or day == "all":
                    break;
                retry -= 1

    print("\nYou have chosen '{}' as day/s".format(day.title()))
    print("\n\nYou have choosen '{}' as City, and '{}' as Month, and '{}' as Day".format(city.title(), month.title(), day.title()))
    print('-'*85)
    print("\nLoading...")

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

     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]  

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print("Here we go the Most common Month as requested.\n'{}'".format(calendar.month_name[most_common_month]))

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print("and then the Most common Day.\n'{}'".format(most_common_day))
        
    # display the most common start hour      
    df['hour'] = df['Start Time'].dt.hour

    common_start_hour = df['hour'].mode()[0]
    print("then the most common Start Hour.\n'{}'".format(common_start_hour))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*85)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("\nand here we go the most common Start Station.\n'{}'".format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("\nthen the most common End Station as below.\n'{}'".format(common_end_station))

    # display most frequent combination of start station and end station trip
    
    start_and_end = (df['Start Station'] + "'--'" + df['End Station']).mode()[0]
    print("\nand then the frequent combination of start station and end station will be\n'{}'".format(start_and_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*85)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_sec = df['Trip Duration'].sum()
    total_time_min = total_time_sec/60
    total_time_hour = total_time_min/60
    print("Here we go the Total Travel Time:\n'{}' hour/s and '{}' minute/s and '{}' second/s.".format(total_time_hour, total_time_min, 
    total_time_sec))

    # display mean travel time
    avg_time_sec = df['Trip Duration'].mean()
    avg_time_min = avg_time_sec/60
    avg_time_hour = avg_time_min/60
    print("\nand then the Average Travel Time:\n'{}' hour/s and '{}' minute/s and '{}' second/s.".format(avg_time_hour, avg_time_min, 
    avg_time_sec))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*85)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("We have the Count of {}".format(user_types))
            
    # Display counts of gender
    if 'Gender' in df:
        # Only access Gender column in this case 
        
        count_of_gender = df['Gender'].value_counts()
        print("\nand now the Count of {}".format(count_of_gender))

    else:
        print("\nGender stats cannot be calculated because Gender does not appear in the dataframe")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        
        earliest_year = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()
        print("\nThe Earliest Year of Birth will be: {}\n".format(int(earliest_year)))
        print("\nThe Most recent Year of Birth will be: {}\n".format(int(most_recent)))
        print("\nThe Most common Year of Birth will be: {}\n".format(int(most_common)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*85)

def raw_data(df):
    
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?\n")
    start_loc = 0
    while (start_loc != "no"):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_display = input("Do you wish to continue?:\n").lower()
        if view_display =="no":
            break;
       

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break;


if __name__ == "__main__":
	main()
