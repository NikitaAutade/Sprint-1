from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import UserProfile,OTP
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def IndexPage(request):
    return render(request, 'index.html')


def AboutPage(request):
    return render(request, 'about.html')


def ContactPage(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        subject = f'From Home Rental Service, {subject}'
        body = f'Hi Admin, \n \n \t {name} is trying to contact you. \n \n \t  email: {email} \n \n \t message: {message} \n\n Thanks, \n Home Rental Service'
        from_email = settings.EMAIL_HOST_USER
        to_email = ['ehouserental.services']
        send_mail(subject, body, from_email, to_email, fail_silently=True)
        sub1 = "Home Rental Service"
        body1 = "Thanks for contacting us. We will get back to you within 48 hrs."
        send_mail(sub1, body1, from_email, [email], fail_silently=True)
    return render(request, 'contact.html')


def ServicesPage(request):
    return render(request, 'services.html') 


def LoginPage(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    msg=''    
    if request.method=='POST':
        uname=request.POST.get('username')
        pwd=request.POST.get('password')
        data=authenticate(username=uname,password=pwd)
        if data != None:
            login(request,data)
            return redirect('profile')
        msg='Incorrect Username or Password'  
    return render(request, 'login.html',{"msg":msg}) 


def Logout(request):
    logout(request)
    return redirect('login')

def SignPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        DOB = request.POST.get('dob')
        profile_pic = request.FILES.get('pic')
        gender=request.POST.get('gender')
        address= request.POST.get('address')
        role = request.POST.get('role')
        
        if pass1!=pass2:
            msg='Password should be same.'
            return render(request,'sign.html',{'msg':msg})
        if len(contact)!=10:
            msg='Contact should be 10 digit.'
            return render(request,'sign.html',{'msg':msg})
        try:
            user=User.objects.create_user(
                username=username,
                email=email,
                password=pass1,
                first_name=first_name,
                last_name=last_name
                )
        except:
            msg='Usename already exist.'
            return render(request,'sign.html',{'msg':msg})
        UserProfile.objects.create(
            user=user,
            profilePicture=profile_pic,
            contact_No=contact,
            address=address,
            gender=gender,
            DOB=DOB,
            verified=True,
            userType = role
            )
        return redirect('/login/')
    return render(request, 'sign.html')


def OwnerSign(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        DOB = request.POST.get('dob')
        profile_pic = request.FILES.get('pic')
        gender=request.POST.get('gender')
        address= request.POST.get('address')
        
        if pass1!=pass2:
            msg='Password should be same.'
            return render(request,'owner-sign.html',{'msg':msg})
        if len(contact)!=10:
            msg='Contact should be 10 digit.'
            return render(request,'owner-sign.html',{'msg':msg})
        try:
            user=User.objects.create_user(
                username=username,
                email=email,
                password=pass1,
                first_name=first_name,
                last_name=last_name
                )
        except:
            msg='Usename already exist.'
            return render(request,'owner-sign.html',{'msg':msg})
        UserProfile.objects.create(
            user=user,
            profilePicture=profile_pic,
            contact_No=contact,
            address=address,
            gender=gender,
            DOB=DOB,
            userType="Owner"
            )
        return redirect('/login/')
    return render(request, 'owner-sign.html')


def ForgotPage(request):
    return render(request, 'forgot.html')    


def SendEmailForForgotPassword(request):
    if request.method == "POST":
        username = request.POST.get('username')
        try:
            # breakpoint()
            user = User.objects.get(username=username)
        except:
            msg='Invalid Username.'
            return render(request, 'forgot.html', {'msg':msg})
        try:
            email = user.email
        except:
            msg='There is no Email Associated with this Account.'
            return render(request, 'forgot.html', {'msg':msg})
        
        otp = OTP.objects.create(user=user)

        body = f'Did you forgot your password ?? No Worries !!!\n\n\nThis is your OTP to get your password reset  {otp.otp}  \n\n\nThank You !'
        subject = 'Forgot Password for House Rental Account'
        from_email = settings.EMAIL_HOST_USER
        to_email = [user.email]
        send_mail(subject, body, from_email, to_email, fail_silently=False)
        return redirect('forgotpassword')
    # return render(request, 'forgot.html')

def ForgotPassword(request):
    msg =''
    
    if request.method == "POST":
        username = request.POST.get('username')
        user_otp = request.POST.get('otp')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')    
        if password1!=password2:
            msg='Password should be same.'
            return render(request,'forgotpassword.html', {'msg':msg})
        try:
            user = User.objects.get(username=username)
        except:
            msg='Invalid Username.'
            return render(request,'forgot.html', {'msg':msg})     
        otp = OTP.objects.filter(user=user).order_by('-created_at').first()
        if str(otp.otp) == user_otp:
            user.set_password(password1)
            user.save()
        return redirect('login')
        msg = 'Please Enter Correct OTP'
    return render(request,'forgotpassword.html', {'msg':msg})         


