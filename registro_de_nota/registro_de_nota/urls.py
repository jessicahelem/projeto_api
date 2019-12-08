"""registro_notas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from registro_de_notas.views import AlunoView, ProfessorView, DisciplinaView, GradeDisciplinaView, GradeAlunoView, \
    Logout

router = DefaultRouter()
router.register(r'alunos', AlunoView)
router.register(r'professores', ProfessorView)
router.register(r'disciplinas', DisciplinaView)
router.register(r'grades', GradeDisciplinaView)
# NESTED URLS-----------------------------------------
diciplina_router = routers.NestedSimpleRouter(router, r'disciplinas', lookup='disciplina')
diciplina_router.register(r'grades', GradeDisciplinaView)
aluno_router = routers.NestedSimpleRouter(router, r'alunos', lookup='aluno')
aluno_router.register(r'grades', GradeAlunoView)


#-----------------------------------------------------

schema_view = get_swagger_view(title='Grade Register API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-docs/', schema_view),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', obtain_auth_token),


]

urlpatterns += router.urls
urlpatterns += diciplina_router.urls
urlpatterns += aluno_router.urls
