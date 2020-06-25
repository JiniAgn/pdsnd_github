import time
import datetime
import pandas as pd
import numpy as np
import calendar as cl

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
                     if city is '', it is not loaded data and go to beginning.
        (int) month - name of the month to filter by, or "all" to apply no month filter
                      0=All, 1=January ... 6=June
        (int -> str) day - name of the day of week to filter by, or "all" to apply no day filter
                     0=All, 1=Monday ... 7=Sunday
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    month = 0
    day = 0
    city_in_msg = "Which city? Type Chicago, New York City or Washington :  "
    wrong_city_msg = "......'{}' is wrong city name."
    wrong_msg = "......'{}' is wrong input."
    month_in_msg = "Which month? Type number (i.e. 0=All, 1=January ... 6=June) :  "
    day_in_msg = "Which day? Type number (i.e. 0=All, 1=Monday ... 7=Sunday) :  "
    
    while True:
        city = input(city_in_msg).lower()
        if city not in (CITY_DATA.keys()):
            print(wrong_city_msg.format(city))
            city=''
            break
    # TO DO: get user input for month (all, january, february, ... , june)
        while True:
            try:
                month = int(input(month_in_msg))    
            except ValueError:
                print("......Choose number between 0 to 6")
                continue
            break
        if (month < 0 or month > 6):
            print(wrong_msg.format(cl.month_name[month]))
            city = '' # break and go back to start
            break
        elif month == 0:
            print("...... No month filter")
        else:
            print("...... {} means {}".format(month, cl.month_name[month]))
        
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            try:
                day = int(input(day_in_msg))
            except ValueError:
                print("...... Choose number between 0 to 7")
                continue
            break
        if day < 0 and day > 7:
            print(wrong_msg.format(cl.day_name[day-1]))
            break
        elif day == 0:
            print("...... No day of week filter\n")
            day = 'all'
            break
        else:
            print("...... {} means {}".format(day, cl.day_name[day-1]))
            day = cl.day_name[day-1]  #######
            break
            

    ## print('-'*60)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #print("load_data function from ", CITY_DATA[city])##
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # convert the Start Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 0:
        df = df[df['month'] == month ]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def display_stats_category(c_title):
    """
    Displays each category of statistics

        Args:
            (str) title_c - title of category
        Retuen:

    """
    disp_len = 60
    disp_space = " "
    disp_hline = "-"
    disp_vline = "|"
    title_len = len(c_title)
    space_len = disp_len - title_len
    if (space_len % 2 != 0):
        c_title += ' '
        space_len -= 1 # subtract one space
    space_len -= 2     # subtract two vlin
    space_len = int(space_len/2)
    print('\n')
    print(disp_hline * disp_len)
    print("{}{}{}{}{}".format(disp_vline, disp_space*space_len, c_title,disp_space*space_len, disp_vline))
    print(disp_hline * disp_len)
            
    return space_len

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
   
    c_title = 'The Most Frequent Times of Travel'
    space_cnt = display_stats_category(c_title)

    start_time = time.time()

    # display the most common month
    # check whether the 'month' column is already filtered or not?
    if( len( df['month'].unique()) > 1 ):
        print(' '*space_cnt+'The most common month is \'{}\'.'.format(cl.month_name[df['month'].mode()[0]]))
    else:
        print(' '*space_cnt+"The data set is already filterd by {}".format(cl.month_name[int(df['month'].unique())]))
    
    # display the most common day of week
    if(len(df['day_of_week'].unique()) > 1):
        print(' '*space_cnt+'The most common day is \'{}\'.'.format(df['day_of_week'].mode()[0]))
    else:
        print(' '*space_cnt+"The data set is already filterd by {}".format(df['day_of_week'].unique()[0]))

    # display the most common start hour
    print(' '*space_cnt+'The most common start hour is \'{}\'.'.format(df['Start Time'].dt.hour.mode()[0]))
    print(' '*space_cnt+'The most common end hour is \'{}\'.'.format(df['End Time'].dt.hour.mode()[0]))

    print("\n(This took %s seconds.)" % round(time.time() - start_time,5))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    c_title = 'The Most Popular Stations and Trip'
    space_cnt = display_stats_category(c_title)

    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is\'{}\'.'.format(df['Start Station'].mode()[0]))
    
    # display most commonly used end station
    print('The most commonly used end station is \'{}\'.'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['Comb Station'] = df['Start Station']+'::'+df['End Station']
    print('The most frequent combination of start station and end station trip is \n \'{}\'.'.format(df['Comb Station'].mode()[0]))
    
    print("\n(This took %s seconds.)" % round(time.time() - start_time,5))


def convert_sec_time (sec_d):
    """
    Gets days, hours, minutes, seconds to show how long it takes 
       Args:
           (int) sec_d - total seconds
       Returns:
           (int) d     - days
           (int) h     - hours
           (int) m     - minutes
           (int) s     - seconds
    """
    time_d = datetime.timedelta(seconds = sec_d)
    d, s = time_d.days, time_d.seconds
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    
    return d,h,m,s

def display_time_format(d,h,m,s):
    """
    Makes string format for days, hours, minutes and seconds
        Args:
           (int) d     - days
           (int) h     - hours
           (int) m     - minutes
           (int) s     - seconds
       Return:
           (str) dp_time - time format
    """
    dp_time = ""
    if d != 0:
        dp_time += "{} days ".format(d)
    if h != 0:
        dp_time += "{} hours ".format(h)
    if m != 0:
        dp_time += "{} minutes ".format(m)
    if s != 0:
        dp_time += "{} second".format(s)
    
    return dp_time


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    c_title = 'Trip Duration'
    space_cnt = display_stats_category(c_title)

    start_time = time.time()
    stats_dt = df['Trip Duration'].describe()
    for i in range(0,len(stats_dt)):
        if i == 0:
            print("{} of tavel time is {}.".format(stats_dt.index[i].title(),stats_dt.get(stats_dt.index[i])))
        else:
            td,th,tm,ts = convert_sec_time(int(stats_dt.get(stats_dt.index[i])))
            print("{} of tavel time is {}.".format(stats_dt.index[i].title(),display_time_format(td,th,tm,ts)))
    
    # display total travel time   
    td,th,tm,ts = convert_sec_time(int( df['Trip Duration'].sum()))
    print("Total travel time is {}.".format(display_time_format(td,th,tm,ts)))
    
    print("\n(This took %s seconds.)" % round(time.time() - start_time,5))

    
def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    #Display a category title of statistic
    c_title = 'User'
    space_cnt = display_stats_category(c_title)

    start_time = time.time()

    # Display counts of user types
    print("USER TYPE\n",df['User Type'].value_counts())

    # Display counts of gender
    col_list = list(df.columns)
    if 'Gender' in col_list:
        print("\nGENDER\n",df['Gender'].value_counts())
    else:
        print("\nThere is no gender data")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in col_list:
        print("\nBIRTH YEAR OLDEST   :",int( df['Birth Year'].min()))
        print("BIRTH YEAR YOUNGEST :", int(df['Birth Year'].max()))
        print("COMMON BIRTH YEAR   :", int(df['Birth Year'].mode()[0]))
    else:
        print("\nThere is no birth year data")
    
    
    print("\n(This took %s seconds.)" % round(time.time() - start_time,5))


def display_raw_data(df):
    """ Displays raw data """
    
    msg_ask = "Would you like to see raw data?(Yes/No)"
    msg_more = "Do you want to see more 5 lines of raw data?(Yes/No)"
    
    c_title = "Display Raw Data"
    space_cnt = display_stats_category(c_title)
    
    i = 0
    j = 5
    
    user_resp = input(msg_ask).lower()
    
    if user_resp != 'yes' and user_resp != 'no':
        print("......I don't know you want to see or not.\n")
    print("Data size is "+str(len(df)))    
    while user_resp == 'yes':
        if i > len(df)-1:
            print("You already see all "+ str(len(df)) +" datas")
            break
        else :
            print("\n")
            print(df.iloc[i:j])
            user_resp = input(msg_more).lower()
            i = j
            j += 5


def main():
    while True:
        city, month, day = get_filters()
        if city != '':
            df = load_data(city, month, day)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()



