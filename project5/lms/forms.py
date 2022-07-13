from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.DateInput):
    input_type = 'time'


class Add_Homework_Form(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea())
    due_date = forms.DateField(widget=DateInput)
    due_time = forms.TimeField(widget=TimeInput)
    desc_file = forms.FileField()


class Submit_Homework(forms.Form):
    homework_file = forms.FileField()


class Give_Score(forms.Form):
    score = forms.IntegerField(min_value=0, max_value=100)
