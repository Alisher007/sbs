from datetime import time
from reservations.models import Table

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
class Test:
    res_id = ''
    is_available = False
    avail = []
    table = []
    timechoice = [time(9, 0),time(9, 15),time(9, 30),time(9, 45),time(10, 0),
                    time(10, 15),time(10, 30),time(10, 45),time(11, 0),
                    time(11, 15),time(11, 30),time(11, 45)]

    timestring = [
        '09:00','09:15','09:30','09:45',
        '10:00','10:15','10:30','10:45',
        '11:00','11:15','11:30','11:45',
        '12:00','12:15','12:30','12:45','13:00'
    ]