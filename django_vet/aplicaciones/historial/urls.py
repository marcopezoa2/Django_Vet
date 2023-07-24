from django.urls import path
from .views import HistoriaListView

app_name = 'historia'

urlpatterns = [
    path('paciente/<int:paciente_id>/', HistoriaListView.as_view(), name='historial'),
]