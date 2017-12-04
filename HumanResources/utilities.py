from datetime import datetime, date, time, timedelta
import calendar
from HumanResources.models import *

class getParameters():
    @classmethod
    def getPeriodNumber(self):
        fecha1 = datetime.now()
        fecha1 = date(fecha1.year,fecha1.month,fecha1.day)
        fecha2 = date(fecha1.year, 1, 1)
        diferencia = fecha1 - fecha2

        return (int(diferencia.days/15)+1)
