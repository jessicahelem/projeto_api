from rest_framework import serializers
from .models import Professor, Aluno, Disciplina, Grade


class AlunoSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Aluno
        fields = ('url', 'pk', 'name', 'username')


class ProfessorSerializers(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Professor
        fields = ('url', 'pk', 'name')


class DisciplinaSerializers(serializers.HyperlinkedModelSerializer):
    professor = serializers.SlugRelatedField(queryset=Professor.objects.all(), slug_field='name')

    class Meta:
        model = Disciplina
        fields = ('url', 'pk', 'name', 'professor')


class GradeSerializers(serializers.HyperlinkedModelSerializer):
    disciplina = serializers.SlugRelatedField(queryset=Disciplina.objects.all(), slug_field='name')
    professor = serializers.SerializerMethodField()
    aluno = serializers.SlugRelatedField(queryset=Aluno.objects.all(), slug_field='name')

    class Meta:
        model = Grade
        fields = ('pk', 'value', 'professor', 'disciplina', 'aluno')

    def get_professor(self, obj):
        qs = Professor.objects.get(pk=obj.disciplina.professor.pk)
        return qs.name