from django import forms
from datetime import time
from reservations.models import Reservation, Avail
from .utils import Test
from django.core.exceptions import ValidationError

class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation

        fields = [
            'table',
            'customer',
            'product',
            'timestart',
            'duration',
            'date'
        ]
    



    def clean(self):
        """ 
        Override the default clean method to check whether this course has
        been already inputted.
        """    
        cleaned_data = self.cleaned_data
        date = cleaned_data.get('date')
        table = cleaned_data.get('table')
        timestart = cleaned_data.get('timestart')
        duration = cleaned_data.get('duration')
        durationInt = int(duration) // 15
        
        availtemp = []
        availStr = ''
        for ii in range(durationInt):
            availStr = str(date) + '_' + Test.timestring[Test.timestring.index(str(timestart)) + ii] + '_' + str(table)
            matching_avail = Avail.objects.filter(name=availStr)
            Test.avail.append(availStr)
            if Test.res_id != '':
                matching_avail = matching_avail.exclude(reservation_id=Test.res_id)
            if matching_avail.exists():
                msg = "Reservation already exists."
                Test.avail = []
                raise ValidationError(msg)
        
        return self.cleaned_data

    

        