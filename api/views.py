from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStudent,IsInstructor
from rest_framework import status, views
from .models import Class,Course
from .seializers import ClassSerializer, CourseSerializer,RegisterSerializer
import json
import io
from django.http import FileResponse
@api_view(['GET'])
@permission_classes([IsAuthenticated,IsInstructor])
def classList(request):
    try:
        classes = Class.objects.all()
        serializer = ClassSerializer(classes,many=True)
        return Response(serializer.data)
    except:
        raise Exception("An error occured")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def courseList(request):
    try:
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    except:
        raise Exception("An error occured")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userInfo(request):
    try:
        id = request.user.id
        is_student = request.user.is_student
        is_instructor = request.user.is_instructor
        return Response({"id":id,"is_student":is_student,"is_instructor":is_instructor})
    except:
        raise Exception("An error occured")

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsInstructor])
def studentList(request):
    try:
        students = CustomUser.objects.filter(is_student=True)
        serializer = CustomUserSerializer(students, many=True)
        return Response(serializer.data)
    except:
        raise Exception("An error occured")

@api_view(['GET'])
@permission_classes([IsAuthenticated,IsStudent])
def studentSingle(request,pk):
    try:
        student = CustomUser.objects.get(id=pk)
        serializer = CustomUserSerializer(student, many=False)
        return Response(serializer.data)
    except:
        raise Exception("An error occured")

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsInstructor])

def createClass(request):
    try:
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=serializer.data)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data=serializer.errors)        
        try:
            classes = Class.objects.all()
            serializer = ClassSerializer(classes,many=True)
            return Response(serializer.data)
        except:
            raise Exception("An error occured")

    except:
        raise Exception("An error occured")

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsStudent])

def chooseCourses(request,pk):
    try:
        student = CustomUser.objects.get(id=pk)
        counter = 0
        id_list = request.data
        courses = Course.objects.filter(pk__in = id_list)
        for course in courses:
            counter+=course.credit
        #student can get courses between 10 to 20 credits total
        if counter >= 10 and counter <= 20:
            student.courselist.set(courses)
            serializer = CourseSerializer(student.courses,many=True)
            if serializer.is_valid:
                return Response(serializer.data)
        elif counter < 10:
            return Response(status=status.HTTP_403_FORBIDDEN, data="please choose more lessons")
        
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data="too many lessons choosen")
    except:
        raise Exception("An error occured")
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsInstructor])

def addStudentToClass(request,pk):
    try:
        classToAdd  = Class.objects.get(id = pk)
        id_list = request.data
        for id in id_list:
            classToAdd.students.add(id)
        try:
            classes = Class.objects.all()
            serializer = ClassSerializer(classes,many=True)
            return Response(serializer.data)
        except:
            raise Exception("An error occured")
    except:
        raise Exception("An error occured")
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsInstructor])

def createCourse(request):
    try:
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=serializer.data,instructor = request.user)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data=serializer.errors)        
        return Response(serializer.data)
    except:
        raise Exception("An error occured")
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsInstructor])

def updateClass(request,pk):
    try:
        classToEdit = Class.objects.get(id=pk) 
        serializer = ClassSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.update(instance=classToEdit,validated_data=request.data)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data=serializer.errors)        
        return Response(serializer.data)
    except:
        raise Exception("An error occured")
@api_view(['POST'])
def createUser(request):
    try:
        reg_serializer = RegisterSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
            if new_user:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    except:
        raise Exception("An error occured")