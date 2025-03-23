from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from review.models import menu,SelectedItems,Casestudy
import emoji
import csv

# Create your views here.
@login_required(login_url='login')
def Homepage(request):
    all_menuthings = menu.objects.values()
    print(all_menuthings)
    if request.method == 'POST':
        items = request.POST.getlist('items')
        uname=request.POST.get('review_pista')
        uname_text = emoji.demojize(uname)
        selected_items = Casestudy(keywords=','.join(items),review_pista=uname_text)
        selected_items.save() 
        
        return redirect('/')
    

    return render(request,'home.html',{'all': all_menuthings})




def SignupPage(request):
     

     if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("password mismatch")
        
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    

     return render (request,'signup.html')
        
                                                                       

def Loginpage(request):
     
     if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('firstpage')
        else:
            return HttpResponse ("Username or Password is incorrect NOOBDA GET GOOD!!!")
        


     return render (request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def HomePage(request):
        if request.method=='POST':
            if 'button1' in request.POST:
                return redirect('solve')
            elif 'button2' in request.POST:
             return redirect('order')

        return render(request, 'homepage.html')
         
@login_required(login_url='login')         
def Order(request):
    if request.method=='POST':
         if 'button1' in request.POST:
            return redirect('update')
         elif 'button2' in request.POST:
            return redirect('add_menu')
         elif 'button3' in request.POST:
            return redirect('home')
         
    return render(request, 'order.html')


def Firstpage(request):
    return render(request, 'firstpage.html')




def load_csv_to_model(csv_file_path):
    with open(csv_file_path, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader) # skip header row
        for row in csv_reader:
            # create model instance and set values from CSV data
            my_model = Casestudy()
            city = row[0]
            my_model.review_pista = row[0]
            if 'burger' in city:
                my_model.keywords = 'burger'
            elif 'haleem' in city:
                my_model.keywords = 'haleem'
            elif 'chicken' in city:
                my_model.keywords = 'chicken'
            elif 'chicken salad' in city:
                my_model.keywords = 'chicken salad'
            elif 'mutton' in city:
                my_model.keywords = 'mutton'
            else:
               my_model.keywords = 'UnKnown'
            # set other fields as needed
            my_model.save()



def load_csv(request):
    csv_file_path = "C:/Users/1902f/Downloads/pistahouse1000_reviews.csv"
    load_csv_to_model(csv_file_path)
    return render(request, 'load_csv.html')
