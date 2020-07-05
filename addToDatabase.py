import os
from os import listdir
import django
from django.conf import settings
from datetime import datetime


os.environ['DJANGO_SETTINGS_MODULE'] = 'covid19.settings'
django.setup()

from web.models import JhuData, VnData, EcdcData

def addVnData():
    dirPath = os.path.join(settings.BASE_DIR, 'data/VN')
    fileNames = listdir(dirPath)
    for fileName in fileNames:
        if 'cities' in fileName:
            data_type = "CT"
        else:
            data_type = "PT"
        date = datetime.strptime(fileName[:10], '%m-%d-%Y')
        if len(VnData.objects.filter(date = date, data_type = data_type)) == 0:
            filePath = 'data/VN/%s' % fileName
            data = VnData(data_type=data_type, date=date, csv_file = filePath)
            data.save()

def addJhuData():
    dirPath = os.path.join(settings.BASE_DIR, 'data/JHU')
    fileNames = listdir(dirPath)
    for fileName in fileNames:
        date = datetime.strptime(fileName[:10], '%m-%d-%Y')
        if len(JhuData.objects.filter(date = date)) == 0:
            filePath = 'data/JHU/%s' % fileName
            data = JhuData(date=date, csv_file = filePath)
            data.save()

def addEcdcData():
    dirPath = os.path.join(settings.BASE_DIR, 'data/ECDC')
    fileNames = listdir(dirPath)
    for fileName in fileNames:
        date = datetime.strptime(fileName[:10], '%m-%d-%Y')
        if len(EcdcData.objects.filter(date = date)) == 0:
            filePath = 'data/ECDC/%s' % fileName
            data = EcdcData(date=date, csv_file = filePath)
            data.save()

def addData():
    addVnData()
    addJhuData()
    addEcdcData()

addData()