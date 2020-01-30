from django.views import View
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .queue import Services
from .pickling import pickle_the_q

EQ = pickle_the_q()


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        # return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')
        return render(request, 'index.html', {'title': "Welcome!"})


class Menu(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'menu.html', {'title': 'Main Menu'})


class Ticket(View):
    def get(self, request, *args, **kwargs):
        ticket_number = EQ.incr_tickt_no()
        EQ.save_state()
        if 'change_oil' in request.path:
            minutes_to_wait = len(EQ.tickets_processing[Services.OIL.value]) * EQ.oil_time
            EQ.tickets_processing[Services.OIL.value].append(ticket_number)
            EQ.save_state()
        elif 'inflate_tires' in request.path:
            minutes_to_wait = len(EQ.tickets_processing[Services.OIL.value]) * EQ.oil_time + len(
                EQ.tickets_processing[Services.TIRES.value]) * EQ.tires_time
            EQ.tickets_processing[Services.TIRES.value].append(ticket_number)
            EQ.save_state()
        elif 'diagnostic' in request.path:
            minutes_to_wait = len(EQ.tickets_processing[Services.OIL.value]) * EQ.oil_time + len(
                EQ.tickets_processing[Services.TIRES.value]) * EQ.tires_time + len(
                EQ.tickets_processing[Services.DIAG.value]) * EQ.diagnostics_time
            EQ.tickets_processing[Services.DIAG.value].append(ticket_number)
            EQ.save_state()
        return render(request, 'to_wait.html',
                      {'ticket_number': ticket_number, 'minutes_to_wait': minutes_to_wait, 'title': "wait estimate"})


class Operator(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'operator.html', {'oil': len(EQ.tickets_processing[Services.OIL.value]),
                                                 'tires': len(EQ.tickets_processing[Services.TIRES.value]),
                                                 'diag': len(EQ.tickets_processing[Services.DIAG.value]),
                                                 'title': "Operator"})

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            EQ.current = 0
            if EQ.tickets_processing[Services.OIL.value]:
                EQ.current = EQ.tickets_processing[Services.OIL.value][0]
                del EQ.tickets_processing[Services.OIL.value][0]
                EQ.save_state()
            elif EQ.tickets_processing[Services.TIRES.value]:
                EQ.current = EQ.tickets_processing[Services.TIRES.value][0]
                del EQ.tickets_processing[Services.TIRES.value][0]
                EQ.save_state()
            elif EQ.tickets_processing[Services.DIAG.value]:
                EQ.current = EQ.tickets_processing[Services.DIAG.value][0]
                del EQ.tickets_processing[Services.DIAG.value][0]
                EQ.save_state()

            return HttpResponseRedirect('/next/')


'''
RuntimeError: You called this URL via POST, but the URL doesn't end in a slash and you have APPEND_SLASH set.
Django can't redirect to the slash URL while maintaining POST data.
Change your form to point to localhost:8000/processing/ (note the trailing slash),
or set APPEND_SLASH=False in your Django settings.
[24/Jan/2020 12:16:58] "POST /processing HTTP/1.1" 500 68092
-> so I added 

Server error 500 in debug=false with csrf_protect decorator
'''


class CurrentTicket(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'current_ticket.html', {'ticket_number': EQ.current})
