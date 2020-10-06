import datetime
import time

def logLoader(path):
    allLines = []
    with open(path) as file:
        for line in file:
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
            timeStamp = self.parseStringToTime(elements[0]) 
        except IndexError:  
            timeStamp = ''

        try: 
            startIndex = logLine.find('[', 0)
            payload = logLine[startIndex:]
        except IndexError:
            payload = ''

        return (timeStamp, payload)

    def parseStringToTime(self, date_args): #date_args = '2020-09-04-18:16:12.1515421'
        try:
            timeString = date_args.replace('T', '-')
            timeString = timeString[0:26] # remove '+02:00' + trim milisec part down

            date = datetime.datetime.strptime(timeString, "%Y-%m-%d-%H:%M:%S.%f")
            return date.timestamp() # convert to UNIX time
        except:
            return ''