from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    name = models.CharField(max_length=70)

    def save(self, *args, **kwargs):
        print("@@@@@@@@@", self.username)
        if not self.has_usable_password():
            self.set_password(self.password)
        super(CustomUser, self).save(*args, **kwargs)


class Professor(CustomUser):
    degree = models.CharField(max_length=30, null=True)

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'


class Aluno(CustomUser):
    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'


class Disciplina(models.Model):
    name = models.CharField(max_length=75)
    professor = models.ForeignKey('Professor', related_name='disciplinas', on_delete=models.CASCADE)


class Grade(models.Model):
    value = models.FloatField()
    year = models.IntegerField(null=True)
    semester = models.IntegerField(null=True)
    disciplina = models.ForeignKey('Disciplina', related_name='grades', on_delete=models.CASCADE)
    aluno = models.ForeignKey('Aluno', related_name='grades', on_delete=models.CASCADE)

