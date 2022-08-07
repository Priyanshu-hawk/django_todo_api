from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions, authentication
from .models import TODO
from .seri import ToDoSeri

class TodoListAppView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):

        # print(request.data)
        todos = TODO.objects.filter(user = request.user.id)
        
        seri = ToDoSeri(todos, many=True)
        print(seri.data)
        return Response(seri.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # print(request.data)
        data = {
            'task': request.data.get('task'),
            'completed': request.data.get('completed'),
            'user': request.user.id
        }
        seri_data = ToDoSeri(data=data)

        if seri_data.is_valid():
            seri_data.save()
            return Response(seri_data.data, status=status.HTTP_201_CREATED)
        return Response(seri_data.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_obj(self, todo_id, user_id):
        try:
            return TODO.objects.get(id=todo_id,user = user_id)
        except TODO.DoesNotExist:
            return None
    
    def get(self,request, todo_id, *args, **kwargs):
        todo_instance = self.get_obj(todo_id=todo_id, user_id=request.user.id)
        print(todo_instance)
        if not todo_instance:
            return Response({"res":"Object Not Exist"},status=status.HTTP_404_NOT_FOUND)
        seri_data = ToDoSeri(todo_instance)
        return Response(seri_data.data,status=status.HTTP_200_OK)
    
    def put(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_obj(todo_id, request.user.id)
        if not todo_instance:
            return Response({"res":"Object Not Exist"},status=status.HTTP_404_NOT_FOUND)
        data = {
            'task': request.data.get('task'),
            'completed': request.data.get('completed'),
            'user': request.user.id
        }

        seri_data = ToDoSeri(instance=todo_instance, data=data, partial = True)
        print(seri_data.initial_data)
        if seri_data.is_valid():
            seri_data.save()
            return Response(seri_data.data, status=status.HTTP_200_OK)
        return Response(seri_data.error_messages, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_obj(todo_id,user_id=request.user.id)
        if not todo_instance:
            return Response({"res":"Object Not Exist"},status=status.HTTP_404_NOT_FOUND)
        todo_instance.delete()
        return Response({'res':'Obj Deleted!!'}, status=status.HTTP_200_OK)


    