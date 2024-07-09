from django.urls import path
from . import views,views2
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from EmployeeApp.views import create_ticket, get_tickets_by_tid, get_tickets_by_username

urlpatterns = [

    # path('get_employees', views.get_employees, name='get_employees'),
    # path('create', views.create_employee, name='create_employee'),
    # # path('<str:id>/', views.get_employee, name='get_employee'),
    # path('get_employee/<str:id>', views.get_employee, name='get_employee'),
    # path('update/<str:id>', views.update_employee, name='update_employee'),
    # path('delete/<str:id>', views.delete_employee, name='delete_employee'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('create', create_ticket, name='create_ticket'),
    path('get_by_tid/<int:tid>', get_tickets_by_tid, name='get_ticket_by_tid'),
    path('get_by_username/<str:username>', get_tickets_by_username, name='get_tickets_by_username'),

]



