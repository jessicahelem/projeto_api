from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import filters, status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions, mixins
from .models import Aluno, Professor, Disciplina, Grade
from .permissions import IsProfessor, IsGradeOwner, IsNotAllowed
from .serializers import AlunoSerializers, ProfessorSerializers, DisciplinaSerializers, GradeSerializers


# Create your views here.

class AlunoView(ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializers
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('name',)
    search_fields = ('^username',)
    ordering_fields = ('name',)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny(), ]
        return [permissions.IsAdminUser(), ]


class ProfessorView(ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializers
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('name',)
    search_fields = ('^username',)
    ordering_fields = ('name',)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny(), ]
        return [permissions.IsAdminUser(), ]


class DisciplinaView(ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializers

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny(), ]
        return [permissions.IsAdminUser(), ]


class GradeDisciplinaView(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializers

    def get_queryset(self):
        try:
            return Grade.objects.filter(disciplina=self.kwargs['disciplina_pk'])
        except KeyError:
            return Grade.objects.all()

    def get_permissions(self):
        try:
            if not self.request.user.pk == Disciplina.objects.get(pk=self.kwargs['discipline_pk']).professor.pk:
                if self.request.method in permissions.SAFE_METHODS:
                    return [IsProfessor(), ]
                else:
                    return [IsNotAllowed(), ]
            else:
                return [IsProfessor(), ]
        except:
            return [IsProfessor(), ]


class GradeAlunoView(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializers

    def get_queryset(self):
        try:
            return Grade.objects.filter(aluno=self.kwargs['aluno_pk'])
        except KeyError:
            return Grade.objects.all()

    def get_permissions(self):
        try:
            if not str(self.request.user.pk) == self.kwargs['aluno_pk']:
                return [IsNotAllowed(), ]
            return []
        except:
            return []

