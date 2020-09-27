import datetime
import time

states = {
      'ON': ['OFF'],
      'OFF': '',
      'ERR': ''
 }

def logLoader(path):
    allLines = []
    with open(path) as file:
        for line in file: #.readline():
            allLines.append(LogLine(line))
    return allLines


class LogLine():
    def __init__(self, logLine):
        self.lineElements = self.getLogLineElements(logLine)

    def GetTimeStamp(self):
        return self.lineElements[0]

    def GetPayLoad(self):
        return self.lineElements[1]
    
    def getLogLineElements(self, logLine):
        elements = logLine.split()
        try:
            timeStamp = self.parseStringToTime(elements[0:3]) 
        except IndexError:  
            timeStamp = ''

        elements = logLine.split('dut:')
        try: 
            payload = elements[1]
        except IndexError:
            payload = ''

        return (timeStamp, payload)

    def parseStringToTime(self, date_args):
        defaultYear = '2020'
        actualMonth = self.getMonthIndex(date_args[0]) 
        day = date_args[1]

        timeOfDayElements = date_args[2].split(':') 
        hour = timeOfDayElements[0]
        minutes = timeOfDayElements[1]
        seconds = timeOfDayElements[2]
        miliseconds = timeOfDayElements[3] + '000'

        timeString = defaultYear + '-' + actualMonth + '-' + day + '-' + hour + ':' + minutes + ':' + seconds + ':' + miliseconds

        date = datetime.datetime.strptime(timeString, "%Y-%m-%d-%H:%M:%S:%f")
        return date.timestamp()

    def getMonthIndex(self, monthName):
        monthIndex = {
            'jan': 1,
            'feb': 2,
            'mar': 3,
            'april': 4,
            'may': 5,
            'jun': 6,
            'jul': 7,
            'aug': 8,
            'sept': 9,
            'oct': 10,
            'nov': 11,
            'dec': 12
        }
        try:
            return str(monthIndex[monthName.lower()]) 
        except:
            return 1

    
def ParseLog(searchTerm, filePath):
    log = logLoader(filePath)
    for logLine in log:
        if logLine.GetPayLoad().find(searchTerm) > 0:
            print(logLine.GetTimeStamp(), logLine.GetPayLoad())

ParseLog('Device State:', './testSources/logfile.log')
