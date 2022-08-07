from rest_framework import serializers
from todo_api.models import TODO

class ToDoSeri(serializers.ModelSerializer):
    class Meta:
        model = TODO
        fields = ['task','timestamp','completed','update','user']
