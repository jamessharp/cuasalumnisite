from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, EmailField, Form
from django import forms
from django.contrib.auth.forms import UserCreationForm
import cuasalumnisite.settings as settings
from cuasalumnisite.home.models import Setting
import datetime

SERVICE_CHOICES = (('RAF', 'Royal Air Force'),
                   ('Army', 'Army'),
                   ('Navy', 'Navy'),
                   ('Other', 'Other'))
    
PAYMENT_CHOICES = (('Online', 'Debit/Credit Card'),
                   ('Cheque', 'Cheque'),
                   ('None', 'No thanks - just register my details'))

# Generate a settings dictionary
settings = {}
for setting in Setting.objects.all():
    settings[setting.name] = setting.value

class Member(models.Model):
    
    user = models.OneToOneField(User)
    
    # Personal
    dob = models.DateField()
    college = models.CharField(max_length=50)
    degree = models.CharField(max_length=50, blank=True, null=True)
     
    # Address details - only first field compulsory.
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, blank=True, null=True)
    address_line_3 = models.CharField(max_length=200, blank=True, null=True)
    town = models.CharField(max_length=200, blank=True, null=True)
    post_code = models.CharField(max_length=20, blank=True, null=True)
    
    # Phone details
    mobile_num = models.BigIntegerField(blank=True, null=True)
    home_num = models.BigIntegerField(blank=True, null=True)
    
    # CUAS details
    cuas_member_from = models.DateField()
    cuas_member_to = models.DateField()
    position_held = models.CharField(max_length=200, blank=True, null=True)
    joined_service = models.BooleanField()
    service_joined = models.CharField(max_length=5, choices=SERVICE_CHOICES, blank=True, null=True)
    service_joined_details = models.CharField(max_length=50, blank=True, null=True)
    service_rank = models.CharField(max_length=50, blank=True, null=True)
    
    # Profession
    profession = models.CharField(max_length=200, blank=True, null=True)
    profession_public = models.BooleanField()
    
    # Payment details
    life_member = models.BooleanField()
    payment_method = models.CharField(max_length=8, choices=PAYMENT_CHOICES)
    expiry_date = models.DateField(blank=True, null=True)
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    
    # Receive newsletters and suchlike
    newsletter = models.BooleanField()
    
    # Userful routines
    def paid_member(self):
        return self.life_member or (self.expiry_date and (datetime.date.today() <= self.expiry_date))
    
class MemberForm(ModelForm):
    class Meta:
        model = Member
        
class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ('email')
    username = EmailField(max_length=75, help_text="Email Address")
    def clean_email(self):
        email = self.cleaned_data['username']
        return email

class MemberSignupFormBasic(Form):
    title = "Email and password"
    description = settings.get("memberSignupBasicFormDescription", "")
    email = EmailField(max_length=75, help_text="Email Address")
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(render_value=True))
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput(), help_text="Confirm Password")
    
    # Check the email is unique
    def clean_email(self):
        email_addr = self.cleaned_data.get('email')
        try:
            User.objects.get(username__iexact=email_addr)
        except:
            return email_addr
        raise forms.ValidationError('This email address already exists')
              
    # Do some custom checking. 
    def clean(self):
        # Check the passwords are uniqe
        pass_a = self.cleaned_data.get('password')
        pass_b = self.cleaned_data.get('confirm_password')
        if pass_a != pass_b:
            raise forms.ValidationError('Passwords must match')
        return self.cleaned_data        
    
    models.SubfieldBase
    
class MemberSignupFormPersonal(Form):
    title = "Personal Details"
    description = settings.get("memberSignupPersonalFormDescription", "")
    
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    date_of_birth = forms.DateField(input_formats=['%d/%m/%Y',], help_text='Format: dd/mm/yyyy')
    
    # Address details - only first field compulsory.
    address_line_1 = forms.CharField(max_length=200)
    address_line_2 = forms.CharField(max_length=200, required=False)
    address_line_3 = forms.CharField(max_length=200, required=False)
    town = forms.CharField(max_length=200, required=False)
    post_code = forms.CharField(max_length=20, required=False)
    
    mobile_num = forms.IntegerField(required=False)
    home_num = forms.IntegerField(required=False)

class MemberSignupFormUni(Form):
    title = "University/CUAS details"
    description = settings.get("memberSignupUniFormDescription", "")
    
    college_or_uni = forms.CharField(max_length=50)
    degree_subject = forms.CharField(max_length=50, required=False)
    
    cuas_member_from = forms.DateField(input_formats=['%d/%m/%Y',], help_text='Format: dd/mm/yyyy. If unsure of date use Jan 1st')
    cuas_member_to = forms.DateField(input_formats=['%d/%m/%Y',], help_text='Format: dd/mm/yyyy. If unsure of date use Jan 1st.')
    position_held = forms.CharField(max_length=200, required=False)
    
class MemberSignupFormWorking(Form):
    title = "Post-CUAS details"
    description = settings.get("memberSignupWorkingFormDescription", "")
    
    joined_service = forms.BooleanField(required=False, label="Joined military service?")
    service_joined = forms.CharField(max_length=5, widget=forms.Select(choices=SERVICE_CHOICES), required=False)
    service_joined_details = forms.CharField(max_length=50, required=False, label="If other, provide details")
    service_rank = forms.CharField(max_length=50, required=False, label="Rank attained")
    
    profession = forms.CharField(max_length=200, required=False)
    
class MemberSignupFormPayment(Form):
    title = "Payment details"
    description = settings.get("memberSignupPaymentFormDescription", "")
    payment_method = forms.CharField(max_length=8, widget=forms.Select(choices=PAYMENT_CHOICES))

