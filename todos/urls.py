from django.contrib import admin
from django.urls import path

admin.site.site_header="DTECH TODOS"
admin.site.site_title="DTECH TODOS"
admin.site.index_title="DTECH TODOS"




urlpatterns = [
    path('', admin.site.urls),
]
