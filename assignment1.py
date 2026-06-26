#!/usr/bin/env python3

'''
OPS445 Assignment 1
Program: assignment1.py 
Author: "Basanta Chand- bchand1"
Semester: "Summer 2026"

The python code in this file (assignment1.py) is original work written by
"Student Name". No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading. I understand
that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.
'''

import sys

def day_of_week(year: int, month: int, date: int) -> str:
    "Based on the algorithm by Tomohiko Sakamoto"
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'] 
    offset = {1:0, 2:3, 3:2, 4:5, 5:0, 6:3, 7:5, 8:1, 9:4, 10:6, 11:2, 12:4}
    if month < 3:
        year -= 1
    num = (year + year//4 - year//100 + year//400 + offset[month] + date) % 7
    return days[num]


def mon_max(month:int, year:int) -> int:
    "returns the maximum day for a given month. Includes leap year check"

    # Calculating the maximum days in February if the given year is leap year or not a leap year
    if month == 2:
        if leap_year(year):
            return 29
        else:
            return 28
        
    # Maximum days for all other months
    month_days = {1:31, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    return month_days[month]

def after(date: str) -> str:
    '''
    after() -> date for next day in YYYY-MM-DD string format

    Return the date for the next day of the given date in YYYY-MM-DD format.
    This function takes care of the number of days in February for leap year.
    This fucntion has been tested to work for year after 1582
    '''
    # Split input date string into year, month, day
    str_year, str_month, str_day = date.split('-')
    
    #COnvert string values to integer
    year = int(str_year)
    month = int(str_month)
    day = int(str_day) 
    
    #MOve to next day
    tmp_day = day + 1  # next day
    

    # Uses mon_max()
    if tmp_day > mon_max(month, year):
        to_day = tmp_day % mon_max(month, year)  # if tmp_day > this month's max, reset to 1 
        tmp_month = month + 1
    else:
        to_day = tmp_day #Stay in same month
        tmp_month = month + 0
    
    #If month goes past December, reset to January and increase year
    if tmp_month > 12:
        to_month = 1
        year = year + 1
    else:
        to_month = tmp_month + 0


    #Return formatted next date string YYYY-MM-DD
    next_date = f"{year}-{to_month:02}-{to_day:02}"

    return next_date


def usage():
    "Print a usage message to the user"
    print("Usage: assignment1.py YYYY-MM-DD YYYY-MM-DD")
    
    sys.exit(1)


def order_dates(date1: str, date2: str):
    #Return dates in correct order

    if date1 <= date2:
        return date1, date2
    else:
        return date2, date1



def leap_year(year: int) -> bool:
    "return True if the year is a leap year"
    #A year divisible by 400 isa always a leap year
    if year % 400 ==0:
        return True
    # A year divisible by 100 (but not 400) is NOT a leap year
    elif year % 100 ==0:
        return False

    # A year divisible by 4 is a leap year
    elif year % 4 ==0:
        return True

    # All other years are not a leap year
    else:
        return False


def valid_date(date: str) -> bool:
    "check validity of date and return True if valid"
    try:
        #SPlit date string into year, month, day
        #Example "2025-09-20" --> "2025", "09", "20"
        year_str, month_str, day_str = date.split("-")

        #Checks if the given date is in valid format (YYYY-MM-DD)"
        #Rejects inputs like "30-09-23" or "2025-1-1"
        if len(year_str) != 4 or len(month_str)!=2 or len(day_str)!=2:
            return False


        #Converts string values into integers
        year=int(year_str)
        month=int(month_str)
        day=int(day_str)


        #Month must be in between 1 and 12
        if month<1 or month>12:
            return False

        #Day must be atleast 1 and cannot exceed the maximum number of days in month
        #mon_max() handles the leap year
        if day<1 or day > mon_max(month,year):
            return False
        
        #All checks passed so the date is valid
        return True
    
    #If anything goes wrong (bad format, letters instead of numbers, etc) the date is invalid
    except:
        return False


def day_count(start_date: str, stop_date: str) -> int:
    "Loops through range of dates, and returns number of weekend days"
    #Variable to store the numbers of Saturdays and Sundays found
    count = 0
    
    #Start checking from the starting date
    current_date=start_date

    #Keep looping until we reach stop date
    while True:

        #Split the current date into year, month, day
        year_str, month_str, day_str = current_date.split("-")
        

        #COnverts the string into integers because day_of_week() requires integer arguments
        year=int(year_str)
        month=int(month_str)
        day=int(day_str)

        #Determine the weekday for the current date. Returns on of:
        #"sun", "mon", "tue", "wed", "thu", "fri", "sat"
        weekday = day_of_week(year,month,day)

        #If the current date is Saturday or Sunday, increase the weekend counter
        
        if weekday == "sat" or weekday == "sun":
            count +=1
        
        #If we have reached the ending date, stop the loop
        #This ensures that the both the satrt and stop dates are included in the count
        if current_date == stop_date:
            break
        current_date=after(current_date)
    return count


if __name__ == "__main__":
     
    #Program should receive exactly two dates
    if len(sys.argv) !=3:
        usage()

    #Get dates from command line
    first_date = sys.argv[1]
    second_date = sys.argv[2]

    #CHeck if both dates are valid
    if not valid_date(first_date):
        usage()

    if not valid_date(second_date):
        usage()

    #Make sure start date comes before end date
    start_date, stop_date = order_dates(first_date, second_date)

    #count and print weekend days
    weekends = day_count(start_date, stop_date)
    print("The period between " + start_date + " and " + stop_date + " includes " + str(weekends) + " weekend days")
