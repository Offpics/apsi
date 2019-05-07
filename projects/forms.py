from django import forms
from django.contrib.auth.models import User
from .models import Project


class ProjectCreateForm(forms.ModelForm):
    """ Form for Project creation.
    This form was created so we can only add users that belong to Group Worker
    through this form. """

    class Meta:
        model = Project
        fields = ['title', 'description', 'worker']

    def __init__(self, *args, **kwargs):
        super(ProjectCreateForm, self).__init__(*args, **kwargs)
        queryset = User.objects.filter(groups__name='Worker')
        self.fields['worker'].queryset = queryset
