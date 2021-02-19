from django.urls import path

from . import views


urlpatterns = [
    path('add/',
         views.AddressGeoDataAddView.as_view()),

    path('delete/',
         views.AddressGeoDataDeleteView.as_view()),

    path('provide/',
         views.AddressGeoDataProvideView.as_view()),

    path('list/',
         views.AddressListView.as_view())
]
