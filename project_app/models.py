from django.db import models


# Create your models here.
class Project(models.Model):
    '''
    项目表
    '''
    name = models.CharField(max_length=50,null=False)
    describe = models.TextField(default="")
    status = models.BooleanField(default=1)
    creat_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
