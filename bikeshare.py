import calendar
import pandas as pd
import time


city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
filter_times    = ['month', 'day', 'both', 'none']
filter_months   = ['january', 'february', 'march', 'april', 'may', 'june', 'none']
filter_days     = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'none']

msg_for_get_filter = {
    'city': 'Would you like to see data for Chicago, New York City , or Washington?\n> ',
    'time': '\nWould you like to filter the data by month, day, both or not at all? Type month, day, both, or none for no time filter\n> ',
    'month':'Which month? Please type January, February, March, April, May, June\n> ',
    'day': 'Which day of the week? mon, tue, wed, thu, fri, sat, sun\n> '
} 

msg_for_invalid_get_filter = {
    'city': '\n\nThe value you entered is not valid - available options:\nChicago, New York City, or Washington\n> ',
    'time': '\n\nThe value you entered is not valid - available options:\nmonth, day, both, or none\n> ',
    'month':'\n\nThe value you entered is not valid - available options:\nJanuary, February, March, April, May, June\n> ',
    'day':  '\n\nThe value you entered is not valid - available options:\nmon, tue, wed, thu, fri, sat, sun\n> ' 
}

No_filter = 'No filter selected'

def get_input(input_valid_msg,input_invalid_msg, list):
    """
    Sets dialogue to the user, until he inputs the correct expected value without breaking the code

    Args:
        (str) - input_valid_msg - message that guides the user on what data to input/supply
        (str) - input_invalid_msg - msg that informs user that his last input was not valid
        (list)- list - of possible valid inputs that can be entered  
    
    Returns:
        (str) - user's chosen option
    """
    val = input(input_valid_msg).lower().strip()
    while val not in list:
        val = input(input_invalid_msg).lower().strip()
    return val

def get_filters():
    """
    Asks user to specify a city, month, or day to analyze.

    Returns:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "none" for no filter per month
        (str) day   - name of the day of week to filter by, or "none" for no filter per day of the week
    """

    while True:
        print('\nHello! Let\'s explore some US bikeshare data!!!!\n')
            
        city = get_input(msg_for_get_filter['city'],msg_for_invalid_get_filter['city'],list(city_data.keys()))
        time_filter = get_input(msg_for_get_filter['time'],msg_for_invalid_get_filter['time'],filter_times)
        
        if time_filter == 'none':
            month = 'none'
            day = 'none'
        elif time_filter == 'month':
            month = get_input(msg_for_get_filter['month'],msg_for_invalid_get_filter['month'], filter_months)   
            day = 'none'
        elif time_filter == 'day': 
            month = 'none'
            day =  get_input(msg_for_get_filter['day'],msg_for_invalid_get_filter['day'], filter_days)          
        elif time_filter == 'both':
            month = get_input(msg_for_get_filter['month'],msg_for_invalid_get_filter['month'], filter_months)
            day =  get_input(msg_for_get_filter['day'],msg_for_invalid_get_filter['day'],  filter_days)

        if month == 'none':
            mon_val = No_filter
        else:
            mon_val = month.title()

        if day == 'none':
            day_val = No_filter
        else:
            day_val = day.title()
        # presenting current options and allowing user to continue or go back to the beginning
        print('\n\n')
        print(f"Currently your selection consists of: City - {city.title()}; Month - {mon_val}; Day - {day_val}")
        choice = input('\nIf you are happy with your choices, please type [yes|y] to continue, any other input will go back to the beginning\n> ').lower().strip()
        
        if  choice in ['yes', 'y']:
            break 
        else:
            continue
    
    print('='*135)
    return city.lower(), month.lower(), day.lower()


def load_data(city, month, day):

    """Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "none" no month filter will be applied
        (str) day   - name of the day of week to filter by, or "none" no filter by day of the week will be applied
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    #getting dataframe based on the chosen city
    filename = city_data[city]
    df = pd.read_csv(filename)

    # converting Start Time column into a datetime 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # adding new columns to the dataframe based on the 
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week
    df['hour'] = df['Start Time'].dt.hour

    # time filters - by month or day of the week
    if month != 'none':
        # dt.month - Jan = 1, need to compensate as within list Jan is zero index
        month = filter_months.index(month) + 1
        df = df.loc[df['month'] == month]

    if day != 'none':
        # dt.day_of_week - Mon = 0, synchronized with list zero index
        day = filter_days.index(day)
        df = df.loc[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #print(df.head(100))
    
    # display the most common start month
    most_common_month = df['month'].mode()[0]
    print(f'The most common start month is: {most_common_month} ({calendar.month_name[most_common_month]})')

    # display the most common day of week
    # get the name of the most common day of the week using the calendar module
    most_common_day = df['day_of_week'].mode()[0]
    print(f'The most common day of the week is: {most_common_day} ({calendar.day_name[most_common_day]})')

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common start hour: ',most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*135)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_deb_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: ',most_common_deb_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is: ',most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_beg_end_st = df[['Start Station', 'End Station']].mode().loc[0]
    print('The most frequent combination of start station and end station trip is: {} and {}'.format(most_common_beg_end_st[0],most_common_beg_end_st[1]))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*135)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time :', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time :', mean_travel_time)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*135)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()

    for user_type, count in user_type_counts.items():
        print('{}: {}'.format(user_type, count))

    # Display counts of genders
    if 'Gender' in df.columns:
        print('\nCounts of genders:')
        count_by_gender = df['Gender'].value_counts()

        for gender, count in count_by_gender.items():
            print('{}: {}'.format(gender,count))
    else:
        print('\nNo stats can be displayed for \'Gender\'.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_years = df['Birth Year']

        # the most common birth year
        most_common_birth_year = birth_years.mode().values[0]
        print("\nThe most common birth year is: {:.0f}".format(most_common_birth_year))
        
        # the most recent birth year
        most_recent_birth_year = birth_years.max()
        print("\nThe most recent birth year is: {:.0f}".format(most_recent_birth_year))

        # the earliest birth year
        earliest_birth_year = birth_years.min()
        print("\nThe earliest birth year is: {:.0f}".format(earliest_birth_year))       
    else:
        print('\nNo stats can be displayed for \'Birth Year\'.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 135)

def display_raw_data(df):
    """Displays raw-data from the dataframe."""

    display_raw_data = input("Would you like to see the first 5 rows of raw data?\nPlease type [yes|y], any other input will be considered \'no\'\n> ")
    
    # beginning of the count
    position = 0

    # while the user keeps inputing yes and there's still data left on teh dataframe
    while display_raw_data.lower() in ['yes','y'] and position < len(df):
        print('\n')
        # display the 5 rwos of data
        print(df.iloc[position:position+5]) #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html#
        position += 5
        # prompt the user if they want to see the next 5 rows
        display_raw_data = input("\nWould you like to see the next 5 rows of raw data? Please type [yes|y], any other input will be considered \'no\'\n> ").strip().lower()

    print('-' * 135)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
    
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
    
        restart = input('\nIf you\'d like to to run again the program, please type [yes|y], any other input will be considered \'no\'\n> ').strip().lower()
        if restart not in ['yes','y']:
            print('\nThank you for having executed the program!\nGood Bye!!!!\n')
            print('='*135)
            print('\n')
            break


if __name__ == '__main__':
	main()
