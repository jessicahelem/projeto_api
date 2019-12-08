import json
import os
import django

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "registro_de_nota.settings")
    django.setup()
    from registro_de_notas.models import Disciplina, Aluno, Grade, Professor

    file = open('./bd1.json')
    data = json.load(file)
    print('carregou file')
    for user in data['professores']:
        print()
        p = Professor.objects.create(name=user['name'],
                                     email=user['email'],
                                     username=user['username'])
        p.set_password('123456')
        p.save()
    for user in data['alunos']:
        print()
        s = Aluno.objects.create(name=user['name'],
                                   email=user['email'],
                                   username=user['username'])
        s.set_password('123456')
        s.save()

    print('Professores e alunos criados\n')

    for disciplina in data['disciplinas']:
        Disciplina.objects.create(name=disciplina['name'],
                                  professor=Professor.objects.get(username=disciplina['professor']))

    print('disciplinas criadas\n')

    for grade in data['grades']:
        Grade.objects.create(
            value=grade['value'],
            year=grade['year'],
            semester=grade['semester'],
            disciplina=Disciplina.objects.get(pk=grade['disciplina']),
            aluno=Aluno.objects.get(username=grade['aluno']))

    print('Notas criadas\n')


if __name__ == '__main__':
    main()
