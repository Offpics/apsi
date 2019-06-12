from datetime import datetime
from crispy_forms.helper import FormHelper

from django import forms
from django.contrib.auth.models import User

from .models import DatePoint, Project, Task


class ProjectCreateForm(forms.ModelForm):
    """ Form for Project creation.
    This form was created so we can only add users that belong to Group Worker
    through this form. """

    class Meta:
        model = Project
        fields = ["title", "description", "worker"]

    def __init__(self, *args, **kwargs):
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        queryset = User.objects.filter(groups__name="Worker")
        self.fields["worker"].queryset = queryset


class DatePointCreateForm(forms.ModelForm):
    worked_date = forms.DateField(
        widget=forms.TextInput(attrs={"type": "date"})
    )

    class Meta:
        model = DatePoint
        fields = ["task", "worked_date", "worked_time", "description", "url"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        pk = kwargs.pop("project_pk")
        super(DatePointCreateForm, self).__init__(*args, **kwargs)
        queryset = Task.objects.filter(project__worker=user).filter(
            project__id=pk
        )
        self.fields["task"].queryset = queryset


class DatePointCreateForm2(forms.ModelForm):

    worked_time = forms.IntegerField(max_value=12, min_value=1)

    class Meta:
        model = DatePoint
        fields = ["task", "title", "worked_time", "description", "url"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        pk = kwargs.pop("project_pk")
        super(DatePointCreateForm2, self).__init__(*args, **kwargs)
        queryset = Task.objects.filter(project__worker=user).filter(
            project__id=pk
        )
        self.fields["task"].queryset = queryset


class QueryDatepointsForm(forms.Form):
    month = forms.ChoiceField(
        widget=forms.Select(),
        choices=[
            ("1", "January"),
            ("2", "February"),
            ("3", "March"),
            ("4", "April"),
            ("5", "May"),
            ("6", "June"),
            ("7", "July"),
            ("8", "August"),
            ("9", "September"),
            ("10", "October"),
            ("11", "November"),
            ("12", "December"),
        ],
        initial=f"{datetime.now().month}",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(QueryDatepointsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
