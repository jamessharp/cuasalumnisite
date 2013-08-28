'''
Created on Jul 25, 2011

@author: james
'''

from django.core.management.base import BaseCommand, CommandError
from cuasalumnisite.members.models import Member
import cuasalumnisite.members.email as email 
import datetime

class Command(BaseCommand):
    help = 'Checks all users to see if they have or are about to expire'
    
    def handle(self, *args, **options):
        
        # Get a list of users who are going to expire today.
        expiring_members = Member.objects.filter(expiry_date__exact=datetime.date.today())
        
        # Get a list of users who are going to expire exactly one week from today.
        weeks_time = datetime.date.today() + datetime.timedelta(7)
        about_to_expire_members = Member.objects.filter(expiry_date__exact=weeks_time)
        
        for member in expiring_members:
            email.send_expiring_message(member.user)
            
        for member in about_to_expire_members:
            email.send_about_to_expire_message(member.user)
            
            