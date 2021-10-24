from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from django.forms import ModelForm
from .models import BookInstance

#если будем возвращать к этому классу, то изменить в views due_back на renewal_date
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Введите дату между настоящим моментом и 4 неделями (по умолчанию 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом).
        if data < datetime.date.today():
            raise ValidationError(_('Недействительная дата - продление в прошлом'))

        #Проверка того, то дата не выходит за "верхнюю" границу (+4 недели).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Недействительная дата - продление более чем на 4 недели вперед'))

        # Помните, что всегда надо возвращать "очищенные" данные.
        return data


class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['renewal_date']

        # Проверка того, что дата не в прошлом
        if data < datetime.date.today():
            raise ValidationError(_('Недействительная дата - продление в прошлом'))

        # Check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Недействительная дата - продление более чем на 4 недели вперед'))

        # Не забывайте всегда возвращать очищенные данные
        return data

    class Meta:
        model = BookInstance
        fields = ['due_back', ]
        labels = {'due_back': _('Дата возврата'), }
        help_texts = {'renewal_date': _('Введите дату между настоящим моментом и 4 неделями (по умолчанию 3).'), }