from django.urls import path
from main.views import CompanyListView,InteractionListView,PartnerListView,InteractionByIDListView

urlpatterns = [
    # path('test/', Home.as_view()),
    path('companies/', CompanyListView.as_view()),
    path('interactions/', InteractionListView.as_view()),
    path('partners/',PartnerListView.as_view()),
    path('interactions/<partner_id>',InteractionByIDListView().as_view())
    #
]
