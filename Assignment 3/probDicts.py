#File: A3 Probability Tables

#This file store the tables given in assignment 3 as dictionaries


pHumidityDict = {('low'):.2,
                ('medium'):.5,
                ('high'):.3}

pTempDict =     {('warm'):.1,
                ('mild'):.4,
                ('cold'):.5}

pIcyDict =      {('low'   ,'warm') :.001,
                ('low'   ,'mild') :.01,
                ('low'   ,'cold') :.05,
                ('medium','warm') :.001,
                ('medium','mild') :.03,
                ('medium','cold') :.2,
                ('high'  ,'warm') :.005,
                ('high'  ,'mild') :.01,
                ('high'  ,'cold') :.35}

pSnowDict =     {('low'   ,'warm'):.0001,
                ('low'   ,'mild'):.001,
                ('low'   ,'cold'):.1,
                ('medium','warm'):.0001,
                ('medium','mild'):.0001,
                ('medium','cold'):.25,
                ('high'  ,'warm'):.0001,
                ('high'  ,'mild'):.001,
                ('high'  ,'cold'):.4}

pDayDict =      {('weekend'):.2,
                ('weekday') :.8}

pCloudyDict =   {('true'):.3,
                ('false'):.9}

pStressDict =   {('false','false'):.01,
                ('false','true') :.2,
                ('true' ,'false'):.1,
                ('true' ,'true') :.5}

pExamsDict =   {('false','false'):.001,
                ('false','true') :.1,
                ('true' ,'false'):.0001,
                ('true' ,'true') :.3}

def pHumidity(val):
        return pHumidityDict[val]
def pTemp(val):
        return pTempDict[val]
def pIcy(humidity,temp):
        return pIcyDict[humidity,temp]
def pSnow(humidity,temp):
        return pSnowDict[humidity,temp]
def pDay(val):
        return pDayDict[val]
def pCloudy(snow):
        return pCloudy[snow]
def pStress(snow,exams):
        return pStressDict[snow,exams]
def pExams(snow,day):
        return pExamsDict[snow,day]

