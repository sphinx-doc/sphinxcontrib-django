from django import forms

from .models import SimpleModel


class SimpleForm(forms.ModelForm):
    test1 = forms.CharField(label="Test1")
    test2 = forms.CharField(help_text="Test2")

    def __init__(self, *args, **kwargs):
        """
        This is a custom init method
        """
        super().__init__(*args, **kwargs)

    class Meta:
        model = SimpleModel
        fields = ("file", "childA", "childrenB", "dummy_field")
