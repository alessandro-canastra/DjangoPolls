"""
Definition of models.
"""

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
import datetime

class Poll(models.Model):
    """A poll object for use in the application views and repository."""
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    author = models.CharField(max_length=100, blank=True)

    def total_votes(self):
        """Calculates the total number of votes for this poll."""
        return self.choice_set.aggregate(Sum('votes'))['votes__sum']

    def __unicode__(self):
        """Returns a string representation of a poll."""
        return self.text

class Choice(models.Model):
    """A poll choice object for use in the application views and repository."""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def votes_percentage(self):
        """Calculates the percentage of votes for this choice."""
        total=self.poll.total_votes()
        return self.votes / float(total) * 100 if total > 0 else 0

    def __unicode__(self):
        """Returns a string representation of a choice."""
        return self.text

class InvoiceManager(models.Manager):
    def create_invoice(self, text, date, invoice_capture, user):
        new_invoice = self.model(text=text, date=date, invoice_capture=invoice_capture, created_by=user)
        new_invoice.save()
        return new_invoice

class Invoice(models.Model):
    """Una factura"""
    text = models.CharField(max_length=200)
    date = models.DateField('date in invoice')
    date_creation = models.DateField('date creation in system',editable=False) #generate automatically on creation
    invoice_capture = models.ImageField(upload_to='images/') 
    created_by = models.ForeignKey(User,models.CASCADE,blank=True,null=True)

    #objects=InvoiceManager()

    def save(self):
        if not self.id:
            self.date_creation = datetime.date.today()
        super(Invoice, self).save()

    def __unicode__(self):
        return self.text

