from datetime import datetime, date, time
import time
import pytz

f = open('opps_times', 'r')
pacific = pytz.timezone('US/Pacific')


def if_available_now(line):

    user_datetime = datetime.now(tz=pacific)
    user_date = user_datetime.date()
    user_time = user_datetime.time()

    line = line.replace(',', '').split(' - ')
    # print line
    start_datetime = line[0].rstrip()
    end_datetime = line[1].rstrip()

    if len(start_datetime) == len(end_datetime):
        
        if (":" in start_datetime) and (":" in end_datetime):
            # Mon Mar 13 2017 10:00 AM Mon Jun 12 2017 12:15 PM
            start_object = datetime.strptime(start_datetime, '%a %b %d %Y %I:%M %p')
            start_date = start_object.date()
            start_time = start_object.time()

            end_object = datetime.strptime(end_datetime, '%a %b %d %Y %I:%M %p')
            end_date = end_object.date()
            end_time = end_object.time()
            # print start_date, "!!!", end_date, "!!!", start_time, "!!!", end_time

        else:
            # Wed Feb 01, 2017 Mon May 01, 2017
            start_object = datetime.strptime(start_datetime, '%a %b %d %Y')
            start_date = start_object.date()
            start_time = start_object.time()

            end_object = datetime.strptime(end_datetime, '%a %b %d %Y')
            end_date = end_object.date()
            end_time = end_object.time()
            # print start_date, "!!!", end_date, "!!!", start_time, "!!!", end_time

    else:
        # Tue Mar 28, 2017, 12:30 PM 03:30 PM
        start_object = datetime.strptime(start_datetime, '%a %b %d %Y %I:%M %p')
        start_date = start_object.date()
        start_time = start_object.time()

        end_object = datetime.strptime(end_datetime, '%I:%M %p')
        end_date = start_date
        end_time = end_object.time()
        # print start_date, "!!!", end_date, "!!!", start_time, "!!!", end_time

    if start_date < user_date and user_date < end_date:
        if start_time < user_time and user_time < end_time:
            return "now!"
        else:
            return "Available today"
    else:
        return "Sorry"


# user date and time



for line in f:
    if ':' in line:
        print if_available_now(line)

    



# print user_date, user_time



# print datetime.now()
# a = "Mon Mar 13 2017"
# date = datetime.strptime(a, '%a %b %d %Y').time()
# time = datetime.strptime(a, '%a %b %d %Y %I:%M %p').time()
# print date