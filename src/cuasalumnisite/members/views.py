from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from models import *
from django.conf import settings
from django.utils.safestring import mark_safe
import urllib2
import urllib
import math
import emailManager

# Paypal forms
class PaypalForms(object):
    
    def __init__(self, request):
        # Set up some generic fields
        user = request.user
        self.paypal_fields = {
            'business': settings.PAYPAL_USERNAME,
            'lc': 'GB',
            'address1': user.member.address_line_1,
            'address2': user.member.address_line_2,
            'city': user.member.town,
            'zip': user.member.post_code,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'currency_code': 'GBP', 
            'button_subtype': 'services',
            'return' : request.build_absolute_uri(reverse('payment_complete_url')),
            'cancel_return': request.build_absolute_uri(reverse('payment_cancel_url')),
            'no_note': '1',
            'no_shipping': '1',
            'custom': user.id,             
            }
        
        self.up_front_form = self.create_up_front_form()
        self.subscription_form = self.create_subscription_form()
    
    def create_basic_form(self, button_url, extra_html=""):
        hidden_inputs_html = "".join(['<input type="hidden" name="%s" value="%s">\n' % (name, value) for name, value in self.paypal_fields.items()])
        
        form_html = """
        <form action="%s" method="post">
        %s
        %s
        <input type="image" src="%s" border="0" name="submit" alt="PayPal - The safer, easier way to pay online.">
        <img alt="" border="0" src="https://www.paypalobjects.com/en_GB/i/scr/pixel.gif" width="1" height="1">
        </form>
        """ % (
            settings.PAYPAL_URL,
            hidden_inputs_html,
            extra_html,
            button_url,
            )
        
        return mark_safe(form_html)
    
    def create_subscription_form(self):
        self.paypal_fields['cmd'] = '_xclick-subscriptions'
        self.paypal_fields['item_name'] = 'Annual Subscription'
        self.paypal_fields['a3'] = '%.2f' % settings.ANNUAL_MEMBERSHIP_COST
        self.paypal_fields['p3'] = '1'
        self.paypal_fields['t3'] = 'Y'
        self.paypal_fields['src'] = '1'
        self.paypal_fields['bn'] = 'CUASAlumni_Subscribe_WPS_GB'
        
        return self.create_basic_form(settings.SUBSCRIBE_BUTTON_URL)

    
    def create_up_front_form(self):
        self.paypal_fields['cmd'] = '_xclick'
        self.paypal_fields['item_name'] = 'Annual/Life Membership'
        self.paypal_fields['bn'] = 'CUASAlumni_BuyNow_WPS_GB'
        self.paypal_fields['option_select0'] = 'Life Membership'
        self.paypal_fields['option_amount0'] = '%.2f' % settings.LIFE_MEMBERSHIP_COST
        self.paypal_fields['option_select1'] = '1 Year'
        self.paypal_fields['option_amount1'] = '%.2f' % settings.ANNUAL_MEMBERSHIP_COST
        self.paypal_fields['option_select2'] = '2 Years'
        self.paypal_fields['option_amount2'] = '%.2f' % (2 * settings.ANNUAL_MEMBERSHIP_COST)
        self.paypal_fields['option_select3'] = '5 Years'
        self.paypal_fields['option_amount3'] = '%.2f' % (5 * settings.ANNUAL_MEMBERSHIP_COST)
        self.paypal_fields['option_select4'] = '10 Years'
        self.paypal_fields['option_amount4'] = '%.2f' % (10 * settings.ANNUAL_MEMBERSHIP_COST)
        self.paypal_fields['option_index'] = '0'
        extra_html = """
        <table>
            <tr><td><input type="hidden" name="on0" value="Membership length">Membership length</td></tr><tr><td><select name="os0">
                <option value="Life Membership">Life Membership, &pound;%.2f</option>
                <option value="1 Year">1 Year, &pound;%.2f</option>
                <option value="2 Years">2 Years, &pound;%.2f</option>
                <option value="5 Years">5 Years, &pound;%.2f</option>
                <option value="10 Years">10 Years, &pound;%.2f</option>
            </select> </td></tr>
        </table>
        """ % (
            settings.LIFE_MEMBERSHIP_COST,
            settings.ANNUAL_MEMBERSHIP_COST,
            settings.ANNUAL_MEMBERSHIP_COST * 2,
            settings.ANNUAL_MEMBERSHIP_COST * 5,
            settings.ANNUAL_MEMBERSHIP_COST * 10,
            )
        
        return self.create_basic_form(settings.PAY_NOW_BUTTON_URL, extra_html=extra_html)
    
    def create_life_form(self):
        self.paypal_fields['cmd'] = '_xclick'
        self.paypal_fields['item_name'] = 'Life Membership'
        self.paypal_fields['bn'] = 'CUASAlumni_BuyNow_WPS_GB'
        self.paypal_fields['amount'] = '%.2f' % settings.LIFE_MEMBERSHIP_COST
        
        return self.create_basic_form(settings.PAY_NOW_BUTTON_URL)

# Create your views here.

def saveRegistration(**kwargs):
    # Arguments are the field values
    
    # Create the user first.
    user = User.objects.create_user(kwargs['email'], kwargs['email'], kwargs['password'])
    user.first_name = kwargs['first_name']
    user.last_name = kwargs['last_name']
    user.full_clean()
    
    member = Member.objects.create(user=user,
                           dob=kwargs['date_of_birth'],
                           college=kwargs['college_or_uni'],
                           degree=kwargs['degree_subject'],
                           address_line_1=kwargs['address_line_1'],
                           address_line_2=kwargs['address_line_2'],
                           address_line_3=kwargs['address_line_3'],
                           town=kwargs['town'],
                           post_code=kwargs['post_code'],
                           mobile_num=kwargs['mobile_num'],
                           home_num=kwargs['home_num'],
                           cuas_member_from=kwargs['cuas_member_from'],
                           cuas_member_to=kwargs['cuas_member_to'],
                           position_held=kwargs['position_held'],
                           joined_service=kwargs['joined_service'],
                           service_joined=kwargs['service_joined'],
                           service_joined_details=kwargs['service_joined_details'],
                           service_rank=kwargs['service_rank'],
                           profession=kwargs['profession'],
                           profession_public=False,
                           life_member=False,
                           payment_method=kwargs['payment_method'],
                           newsletter=False,
                           )
    member.full_clean()
    user.save()
    member.save()
    
    # Sign up the user to the email group
    params = { 
               'email': user.email,
               'fullname': '%s %s' % (user.first_name, user.last_name)
             }
             
    f = urllib.urlopen('https://mailman-mail5.webfaction.com/subscribe/cuasalumni-all', urllib.urlencode(params))
    f.read()
    
def updateRegistration(user, **kwargs):
    # Arguments are the field values
    
    user.email = kwargs['email']
    user.username = kwargs['email']
    user.first_name = kwargs['first_name']
    user.last_name = kwargs['last_name']
    
    if kwargs.has_key('password'):
        user.set_password(kwargs['password'])
        
    member = user.member
    
    member.dob=kwargs['date_of_birth']
    member.college=kwargs['college_or_uni'],
    member.degree=kwargs['degree_subject'],
    member.address_line_1=kwargs['address_line_1'],
    member.address_line_2=kwargs['address_line_2'],
    member.address_line_3=kwargs['address_line_3'],
    member.town=kwargs['town'],
    member.post_code=kwargs['post_code'],
    member.mobile_num=kwargs['mobile_num'],
    member.home_num=kwargs['home_num'],
    member.cuas_member_from=kwargs['cuas_member_from'],
    member.cuas_member_to=kwargs['cuas_member_to'],
    member.position_held=kwargs['position_held'],
    member.joined_service=kwargs['joined_service'],
    member.service_joined=kwargs['service_joined'],
    member.service_joined_details=kwargs['service_joined_details'],
    member.service_rank=kwargs['service_rank'],
    member.profession=kwargs['profession'],
    
    member.save()
    user.save()

def payment(request):
    # First work out what payment type the user has requested...
    user = request.user
    changed = False
    
    #redirect to the login page if the user isn't authenticated
    if not user.is_authenticated():
        return redirect('login_url')
        
    if request.method == 'POST':
        payment_form = MemberSignupFormPayment(request.POST)
        if payment_form.is_valid():
            member = user.member
            member.payment_method = payment_form.cleaned_data['payment_method']
            member.save()
            changed = True
    else:
        payment_form = MemberSignupFormPayment()
    
    # User is logged in - get the payment method.
    payment_method = user.member.payment_method
    paypal_forms = None
    if payment_method == "Online":
        paypal_forms = PaypalForms(request)

    return render_to_response('members/payment.html',
                              {'payment_method': payment_method,
                               'payment_form': payment_form,
                               'payment_method_changed': changed,
                               'paypal_forms' : paypal_forms,
                              },
                              context_instance=RequestContext(request))

def payment_complete(request):
    
    # Payment is supposedly complete. Query Paypal to ensure that everything is cosher
    success = False
    params = {}
    user = request.user
    if request.method == 'GET':
        # Paypal should have returned a tx parameter on the get
        tx = request.GET.get('tx', '')
        if tx != '':
            # Send a post request to paypal requesting the transaction information.
            data_values = {'tx': tx,
                           'cmd': '_notify-synch',
                           'at': settings.PAYPAL_PDT_IDENTITY_TOKEN,
                          }
            post_data = urllib.urlencode(data_values)
            paypal_request = urllib2.Request(settings.PAYPAL_URL, post_data)
            response = urllib2.urlopen(paypal_request)
            response_txt = urllib.unquote_plus(response.read())
            
            # Split the response into lines
            responses = response_txt.splitlines()
            success = responses[0] == "SUCCESS"
            
            if success:
                # Split the rest of the parameters into dictionary.
                params = dict(item.split('=') for item in responses[1:])     
            
                # Check the payment parameters are as we'd expect
                if ((params['receiver_email'] != settings.PAYPAL_USERNAME) or
                    (params['payment_status'] != "Completed")):
                    success = False
                else:
                
                    # The response seems to check out, so store the information
                    amount_paid = float(params['mc_gross'])
                    num_years = 0
                
                    user.member.transaction_id = tx
                
                    # If the amount is over 30GBP then assume life membership
                    if amount_paid >= settings.LIFE_MEMBERSHIP_COST:
                        user.member.life_member = True
                    else:
                        # Not life membership so calculate the number of years on the subscription
                        num_years = amount_paid / float(settings.ANNUAL_MEMBERSHIP_COST)
                        whole_years = int(math.floor(num_years))
                        extra_days = int(365 * (num_years - whole_years))
                    
                        # Calculate the expiry date
                        today = datetime.date.today()
                        expiry_date = today.replace(year=(today.year + whole_years))
                        expiry_date = expiry_date + datetime.timedelta(days=extra_days)
                        user.member.expiry_date = expiry_date
                    
                    user.member.save() 
            
    return render_to_response('members/payment_complete.html',
                              {'success' : success,
                               'params' : params,
                              },
                              context_instance=RequestContext(request))

def payment_cancelled(request):
    
    return render_to_response('members/payment_cancelled.html',
                              context_instance=RequestContext(request))
       
def signup(request):
    
    error_text = None
    
    # If this is a postback then handle it.
    if request.method == 'POST':
        member_form_basic = MemberSignupFormBasic(request.POST)
        member_form_personal = MemberSignupFormPersonal(request.POST)
        member_form_uni = MemberSignupFormUni(request.POST)
        member_form_working = MemberSignupFormWorking(request.POST)
        member_form_payment = MemberSignupFormPayment(request.POST)
        
        form_list = [member_form_basic,
                     member_form_personal,
                     member_form_uni,   
                     member_form_working,
                     member_form_payment,
                    ]
        
        # Validate all the forms
        all_valid = True
        for form in form_list:
            if not form.is_valid():
                all_valid = False
        
        # If everything is valid in the forms then try and save the registration.
        if all_valid:
            # Generate the dictionary of arguments to pass to saveRegistration
            reg_args = {}
            for form in form_list:
                reg_args.update(form.cleaned_data)
            try:
                
                
                saveRegistration(**reg_args) 
                
                # (Check that we can) Log the user in
                user = authenticate(username=reg_args['email'], password=reg_args['password'])
                login(request, user)
                
                # Send an email with registration details.
                emailManager.send_registered_message(user)
                
                # Redirect to the payment page
                return redirect('payment_url')
            
            except Exception, e:
                # Try deleting the registration but return the form for them to try again
                try:
                    user = User.objects.get(username__iexact=reg_args['email'])
                    user.delete()
                except:
                    pass
                error_text = str(e)
        
    else:
        member_form_basic = MemberSignupFormBasic()
        member_form_personal = MemberSignupFormPersonal()
        member_form_uni = MemberSignupFormUni()
        member_form_working = MemberSignupFormWorking()
        member_form_payment = MemberSignupFormPayment()
    
        form_list = [member_form_basic,
                     member_form_personal,
                     member_form_uni,   
                     member_form_working,
                     member_form_payment,
                    ] 
            
    
    return render_to_response('members/signup.html',
                              {'form_list': form_list,
                               'error_text': error_text},
                              context_instance=RequestContext(request))

@login_required    
def account(request):
    
    error_text = None
    user = request.user
    
    # If this is a postback then handle it.
    if request.method == 'POST':
        member_form_basic = MemberSignupFormBasic(request.POST)
        member_form_personal = MemberSignupFormPersonal(request.POST)
        member_form_uni = MemberSignupFormUni(request.POST)
        member_form_working = MemberSignupFormWorking(request.POST)
        member_form_payment = MemberSignupFormPayment(request.POST)
        
        form_list = [member_form_basic,
                     member_form_personal,
                     member_form_uni,   
                     member_form_working,
                     member_form_payment,
                    ]
        
        # Validate all the forms
        all_valid = True
        for form in form_list:
            if not form.is_valid():
                all_valid = False
        
        # If everything is valid in the forms then try and save the registration.
        if all_valid:
            # Generate the dictionary of arguments to pass to saveRegistration
            reg_args = {}
            for form in form_list:
                reg_args.update(form.cleaned_data)
            try:
                
                
                saveRegistration(**reg_args) 
                
                # Redirect to the payment page
                return redirect('payment_url')
            
            except Exception, e:
                # Try deleting the registration but return the form for them to try again
                try:
                    user = User.objects.get(username__iexact=reg_args['email'])
                    user.delete()
                except:
                    pass
                error_text = str(e)
        
    else:
        member_form_basic = MemberSignupFormBasic()
        member_form_personal = MemberSignupFormPersonal()
        member_form_uni = MemberSignupFormUni()
        member_form_working = MemberSignupFormWorking()
        member_form_payment = MemberSignupFormPayment()
    
        form_list = [member_form_basic,
                     member_form_personal,
                     member_form_uni,   
                     member_form_working,
                     member_form_payment,
                    ] 
            
    
    return render_to_response('members/signup.html',
                              {'form_list': form_list,
                               'error_text': error_text},
                              context_instance=RequestContext(request))
    