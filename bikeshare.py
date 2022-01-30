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
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # Making sure, that user can only make valid inputs by checking if the input matches with one entry in the list 
    while True: 
        city = input('\nWould you see data for Chicago, New York City or Washington? \n').lower()
        if city in CITY_DATA:
            break
        else:
            print('Ooops, that does not work. Make sure to write one of the stated City names.')


    # Get user input for month (all, january, february, ... , june)
    # Making sure, that user can only make valid inputs by checking if the input matches with one entry in the list
    while True:
        month = input('\nPlease state a month from January to June. If you do not want to specify a month, enter "all": \n').lower()
        month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all' ]
        if month in month_list:
            break
        else:
            print('Ooops, that does not work. Please try again and enter a month (January to June) or "all".')

            
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    # Making sure, that user can only make valid inputs by checking if the input matches with one entry in the list
    while True:
        day = input('\nPlease state a day from Monday to Sunday. If you do not want to specify a day, enter "all": \n').lower()
        day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        if day in day_list:
            break
        else:
            print('Ooops, that does not work. Please try again and enter a day or "all".')


    print('-'*40)
    return city, month, day

city, month, day = get_filters()


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
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        # filter by month to create the new dataframe
        df = df[(df.month == month)]

        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[(df.day_of_week == day)]

    return df

df = load_data(city, month, day)
#DataFrame for the row data output (without the two new created columns); Dropping the two columns
df_raw = df.drop(['month','day_of_week'],axis=1)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    # Display only most common month, if users choose "all"
    if month == 'all':
        most_common_month = df['month'].mode()[0]
        # Changing the month-number in the corresponding month-name with help of a dictionary
        month_dict = {1: 'January', 2:'February', 3:'March', 4: 'April',5: 'May', 6:'June'}
        print('The most common month is: ' ,month_dict[most_common_month])        
       

    # Display the most common day of week
    # Display only most common day, if users choose "all"
    if day == 'all':
        most_common_day = df['day_of_week'].mode()[0] 
        print('The most common day of the week is: ',most_common_day.title()) 

        
    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print('The most common hour (24-hour format) of the week is: ', most_common_start_hour)
    
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

time_stats(df)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used Start Station is: ',most_common_start_station)

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most commonly used End Station is: ', most_common_end_station)

    # Display most frequent combination of start station and end station trip
    most_popular_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most frequent combination is from', most_popular_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

station_stats(df)
    
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Changing the format of the column 'End Time'
    df['End Time'] = pd.to_datetime(df['End Time'])
    # Creating new column by substracting the column 'End Time' with 'Start Time' to get the Duration in days hh/mm/ss
    df['Trip Time'] = df['End Time'] - df['Start Time']
    
    # Display total travel time
    total_travel_time = df['Trip Time'].sum()
    print('The total travel time is: ',total_travel_time)
    
    # Display mean travel time
    # Rounding the mean time to seconds for better readability, Source: https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.round.html
    mean_travel_time = df['Trip Time'].mean().round(freq='s')
    print('The mean travel time is: ',mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

trip_duration_stats(df)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_types)
    
    # Display counts of gender
    # Because Data in Washington do not include gender, only calculate gender for Chicago and New York
    # Break immediately if city = "washington"
    # Include KeyError exception for safety
    while True:
        try:
            if city == 'washington':
                break
            elif city == 'chicago'or city == 'new york city':
                gender_types = df['Gender'].value_counts()
                print('\nCounts of Gender: \n',gender_types)
                break
            else:
                break
        except:
            print('no "gender" column in data washington')
            break
            
    # Display earliest, most recent, and most common year of birth
    # Because Data in Washington do not include gender, only calculate gender for Chicago and New York
    # Break immediately if city = "washington"
    # Include KeyError exception for safety
    while True:
        try:
            if city == 'washington':
                break
            elif city == 'chicago' or city == 'new york city':
                min_birth = df['Birth Year'].min()
                max_birth = df['Birth Year'].max()
                most_common_year = df['Birth Year'].mode()[0]
                print('\nYear of birth:\n','Earliest: ', min_birth, '\nMost recent: ', max_birth,'\nMost Common:', most_common_year)
                break
            else:
                break

        except:
            print('no "birth year" column in data washington')
            break
            

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

user_stats(df)


def raw_data(df_raw):
    """Displays 5 rows of Raw Data, if users want to see them.
    
    Args:
        df_raw - DataFrame with the raw datas without the supporting columns "month" and "day of the week"
        """
    #Display all the columns in the dataframe
    pd.set_option('display.max_columns',200)
    # Making sure, that user can only make valid inputs by checking if the input matches with one entry in the list
    while True:
        raw_data_slice = input('Do you want to see 5 rows of the raw data? Enter "yes" or "no": \n').lower()
        answers = ['yes','no']
        if raw_data_slice in answers:
            #If user want to see raw data...
            if raw_data_slice == 'yes':
                #...print 5 rows and keep tracking of the iteration. Make sure iteration will stop when reaching final row
                iteration = 0
                while iteration <= df_raw.shape[0]: 
                    print('\n',df_raw.iloc[iteration:iteration+5])
                    iteration += 5
                    #after printing first 5 rows, ask if user want to see another 5 rows and make sure input is valid
                    while True:
                        another_five_rows = input('Do you want to see 5 more rows of the raw data? Enter "yes" or "no": \n').lower()
                        answers_another_rows = ['yes','no']
                        if another_five_rows in answers_another_rows:
                            break
                        
                        else: 
                            print('Ooops, that still does not work. Please try again and enter either "yes" or "no".')
                    #if input of subsequent question is valid, make sure to end iteration if user input is "no"
                    if another_five_rows == 'no':
                        break
            #if first question is valid and inner loops are done, leave the first while loop           
            break
            
        else:
            print('Ooops, that does not work. Please try again and enter either "yes" or "no".')
    
raw_data(df_raw)

# Restart program. Again, only if  input values are yes or no
def restart():
    '''Ask user, if programm should be exit
    returns - restart value'''
    
    while True:
        restart_options = ['yes', 'no']
        restart_value = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart_value in restart_options:
            break
        else:
            print('Ooops, that does not work. Please try again and enter either "yes" or "no".')
    return restart_value

restart_value = restart()
#Exit, if user chooses no
if restart_value == 'no':
    exit()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        #Dropping the 2 created columns for the raw data input
        df_raw = df.drop(['month','day_of_week'],axis=1)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df_raw)
        
        #altered the last part to meet the criteria of valued inputs
        restart_value = restart()
        if restart_value == 'no':
            break

            
if __name__ == "__main__":
    main()
