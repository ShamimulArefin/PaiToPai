from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
   # path('dashboard/', views.summary_dashboard, name='dashboard'),

   # categories
   path('categories/', views.category_list, name='category_list'),
   path('categories/<slug:slug>', views.category_detail, name='category_detail'),
   path('categories/add/', views.add_category, name='add_category'),
   path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
   path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
   
   # expenses
   path('', views.expense_list, name='expense_list'),
   path('add/', views.add_expense, name='add_expense'),
   path('edit/<int:pk>/', views.edit_expense, name='edit_expense'),
   path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
]