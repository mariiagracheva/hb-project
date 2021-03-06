from datetime import datetime, date, time
import time
import pytz

f = open('opps_times', 'r')
pacific = pytz.timezone('US/Pacific')


def format_time(line):
    if '-' in line:
        # user_datetime = datetime.now(tz=pacific)
        # user_date = user_datetime.date()
        # user_time = user_datetime.time()

        try:
            line = line.replace(',', '').split(' - ')
            start_datetime = line[0].rstrip()
            end_datetime = line[1].rstrip()
        except:
            return line

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
        return str(start_date) + "|" + str(end_date) + "|" + str(start_time) + "|" + str(end_time)
    
    else:
        return str(line)

    # if start_date < user_date and user_date < end_date:
    #     if start_time < user_time and user_time < end_time:
    #         print "now!"
    #     else:
    #         print "Available today"
    # else:
    #     print "Sorry"


# user date and time



# for line in f:
        # print format_time(line)

    



# print user_date, user_time



# print datetime.now()
# a = "Mon Mar 13 2017"
# date = datetime.strptime(a, '%a %b %d %Y').time()
# time = datetime.strptime(a, '%a %b %d %Y %I:%M %p').time()
# print date