from django.forms import ModelForm
from moudle_app.models import Module


# 表单
class ModuletForms(ModelForm):
    # name = forms.CharField(label="名称",max_length=100)
    # describe = forms.CharField(label="描述", widget=forms.Textarea)
    # status = forms.BooleanField(label="状态",required=True)

    class Meta:
        model = Module
        fields = ['project', 'name', 'describe']
