from datetime import datetime
import time  

# def ConvertStringToTime(self, date_args): #date_args = '2020-09-04-18:16:12.1515421' '2020-09-29T08:42:42.0346299+02:00'
#     try:
#         timeString = date_args.replace('T', '-')
#         timeString = timeString[0:26] # remove '+02:00' + trim milisec part down

#         date = datetime.datetime.strptime(timeString, "%Y-%m-%d-%H:%M:%S.%f")
#         return date.timestamp() # convert to UNIX time
#     except:
#         e = sys.exc_info()[0]
#         return ''

date_args = '2020-09-29T08:42:42.0346299+02:00'
timeString = date_args.replace('T', '-')
timeString = timeString[0:26] # remove '+02:00' + trim milisec part down

date = datetime.strptime(timeString, "%Y-%m-%d-%H:%M:%S.%f")
print(date)