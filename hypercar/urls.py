"""hypercar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from tickets.views import WelcomeView, Menu, Ticket, Operator, CurrentTicket


urlpatterns = [
    url(r'^$', WelcomeView.as_view(), name="index"),
    path('welcome/', WelcomeView.as_view()),
    path('menu/', Menu.as_view(), name="menu"),
    path('get_ticket/change_oil', Ticket.as_view()),
    path('get_ticket/inflate_tires', Ticket.as_view()),
    path('get_ticket/diagnostic', Ticket.as_view()),
    path('processing/', Operator.as_view(), name="processing"),
    path('next/', CurrentTicket.as_view()),
]
