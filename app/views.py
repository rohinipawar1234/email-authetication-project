from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from project import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request,"index.html")


def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        pass1=request.POST['pass1']

        user=authenticate(username=username,password=pass1)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,"index.html",{'fname':fname})
        else:
            messages.error(request,'bad credentials') 

    return render(request,"signin.html")               
    

def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,'username is alredy exists! please try another one')
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request,'email is alredy exists!')
            return redirect('home')


        if len(username)>10:
            messages.error(request,'username must be under 10 character')

        if pass1!=pass2:
            messages.error(request,'password did not match')

        if not username.isalnum:
            messages.error(request,'username must be alpha-numeric')
            return redirect('home')

        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname  

        myuser.save() 

        messages.success(request,'Your account has been created.we have sent u confirmation mail')



        #Welcome Email

        subject = "Welcome to Orange City!!"
        message = "Hello "+ myuser.first_name + "!! \n" + "Welcome to Pune!! \nThank you for visiting our City. \n\n Thanking You\n Rohini Pawar"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email, to_list, fail_silently=True)


        return redirect('signin')

    return render(request,"signup.html")



def signout(request):
    logout(request)
    messages.success(request,"Logout successfully!")
    return redirect('home')    
           
    


        
     
