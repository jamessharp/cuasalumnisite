'''Module defining email routines for members
'''

from django.core.mail import EmailMultiAlternatives
from cuasalumnisite.home.models import Setting
from django.template.loader import get_template_from_string
from django.template import Context

# Generate a settings dictionary
settings = {}
for setting in Setting.objects.all():
    settings[setting.name] = setting.value
    
def send_message(message_type, user):
    subject = settings.get('%sEmailSubject' % message_type, '')
    from_email = 'web@cuas-alumni.org.uk'
    to = user.email
        
  #  context = Context({'user', user})
        
  #  text_content = get_template_from_string(settings.get('%sEmailPlainText' % message_type, '')).render(context)
  #  html_content = get_template_from_string(settings.get('%sEmailHTMLText' %  message_type, '')).render(context)
  #  print text_content
  #  print html_content
  #  msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
  #  msg.attach_alternative(html_content, 'text/html')
  #  msg.send()

def send_registered_message(user):
    send_message('registered', user)
    
def send_about_to_expire_message(user):
    send_message('aboutToExpire', user)

def send_expiring_message(user):
    send_message('expiring', user)