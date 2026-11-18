from django.urls import path
from . import views

urlpatterns = [
    path('' , views.NoteListView.as_view() , name = 'note_list'),
    path('note/create' ,views.NoteCreateView.as_view() ,name= 'note_create'),
    path('note/<int:pk>' , views.NoteUpdateView.as_view() , name='note_update'),
    path('note/delete/<int:pk>' , views.NoteDeleteView.as_view() , name='note_delete'),
    path('category/create', views.CategoryCreateView.as_view() ,name='category_create'),
    path('category/delete/<int:pk>' , views.CategoryDeleteView.as_view() , name='category_delete'),
    path('download/<int:pk>' , views.download_image , name = 'note_image_download'),
    path('image/remove/<int:pk>' , views.note_image_remove , name='note_image_remove'),
    path('dashboard' , views.dashboard , name="dashboard"),
    path('export' , views.export_system),
    path('getNews', views.getLatestNewsInternet , name = 'note_news'),
    path('getData', views.save_news , name = 'note_news_data'),
    path('ai/tasks', views.ai_tasks, name="ai_tasks"),
    path('ai/chatbot' , views.ai_chatbot , name='ai_chatbot'),
]
