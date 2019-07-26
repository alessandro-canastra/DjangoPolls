"""
Definition of views.
"""

import json
from os import path
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import ListView, DetailView
from app.models import Choice, Poll, Invoice
from .forms import *

class PollListView(ListView):
    """Renders the home page, with a list of all polls."""
    model = Poll

    def get_context_data(self, **kwargs):
        context = super(PollListView, self).get_context_data(**kwargs)
        context['title'] = 'Polls'
        context['year'] = datetime.date.today().year
        return context

class PollDetailView(DetailView):
    """Renders the poll details page."""
    model = Poll

    def get_context_data(self, **kwargs):
        context = super(PollDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Poll'
        context['year'] = datetime.date.today().year
        return context

class PollResultsView(DetailView):
    """Renders the results page."""
    model = Poll

    def get_context_data(self, **kwargs):
        context = super(PollResultsView, self).get_context_data(**kwargs)
        context['title'] = 'Results'
        context['year'] = datetime.date.today().year
        return context

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.date.today().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.date.today().year,
        }
    )

def vote(request, poll_id):
    """Handles voting. Validates input and updates the repository."""
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'app/details.html', {
            'title': 'Poll',
            'year': datetime.date.today().year,
            'poll': poll,
            'error_message': "Please make a selection.",
    })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('app:results', args=(poll.id,)))

def invoice_image_view(request): 
  
    if request.method == 'POST': 
        form = InvoiceForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            temp_post = form.save() 
            temp_post.created_by = request.user;
            temp_post.save()
            return HttpResponseRedirect('success') 
    else: 
        form = InvoiceForm() 
    return render(request, 'app/invoice.html', {
                      'title': 'Poll',
                      'year': datetime.date.today().year,
                      'form' : form}) 
  
  
def success(request): 
    return HttpResponse('successfuly uploaded') 

@permission_required('app.view_Invoice')
def display_invoice_images(request): 
  
    if request.method == 'GET': 
  
        # getting all the objects of hotel. 
        invoices = Invoice.objects.all()  
        return render(request, 'app/display_invoice.html', 
                     {'title': 'Poll',
                      'year': datetime.date.today().year,
                      'invoice_images' : invoices})

@login_required
def seed(request):
    """Seeds the database with sample polls."""
    samples_path = path.join(path.dirname(__file__), 'samples.json')
    with open(samples_path, 'r') as samples_file:
        samples_polls = json.load(samples_file)

    for sample_poll in samples_polls:
        poll = Poll()
        poll.text = sample_poll['text']
        poll.pub_date = timezone.now()
        poll.save()

        for sample_choice in sample_poll['choices']:
            choice = Choice()
            choice.poll = poll
            choice.text = sample_choice
            choice.votes = 0
            choice.save()

    return HttpResponseRedirect(reverse('app:home'))
