from django.shortcuts import render,HttpResponse,redirect
from review.models import menu,SelectedItems,Casestudy
from .forms import add_menu
from .utils import preprocess_text
from .utils1 import preprocess_text2
from django.contrib.auth.decorators import login_required
import array as arr


@login_required(login_url='login')
# Create your views here.
def UpdatePage(request):
   all_menuthings = menu.objects.values()
   return render (request,'update_menu.html',{'all': all_menuthings})
@login_required(login_url='login')
def Add_Menu(request):
     
     if request.method=='POST':
        item_name=request.POST.get('item_name')
        item_price=request.POST.get('item_price')
        my_user=menu(item_name = item_name,item_price = item_price)
        my_user.save()
        return redirect('add_menu')
    

     return render (request,'add_menu.html')
@login_required(login_url='login')
def Solve(request):
    b = [] 
    a = []

    
    if request.method == 'POST':
        diff = Casestudy.objects.filter(review_pista__isnull=False )

        for data in diff:     
            if not data.processed:
                b.append(data.review_pista)
                new_review = str(data.review_pista)
                preprocess_data1 = preprocess_text(new_review)
                preprocess_data3 = preprocess_text2(new_review)
                a.append(preprocess_data1)
                if preprocess_data1=="Positive":
                    data.processed="Positive"
                else:
                    data.processed="Negative"
                if preprocess_data3=="Positive":
                    data.sarcasm="Non-Sarcastic"
                else:
                    data.sarcasm="Sarcastic"
                print(preprocess_data3)
                data.save()
            else:
                pass
        return redirect('chart')   


    return render(request, 'maintemp.html') 


   
def chart1(request):
    positive_count = 0    
    negative_count = 0
    count_p = 0
    count_n = 0
    Non = 0
    yes = 0
    items = menu.objects.values()
    Casestudy1 = Casestudy.objects.filter(keywords__isnull=False)
    item_list = [item['item_name'] for item in items]
    item_counts = {}
    for item in item_list:
        for y in Casestudy1:
            if y.keywords == item:
                if y.processed == 'positive':
                    count_p += 1
                else:
                    count_n += 1
        '''item_counts.append({item+'p': count_p, item+'n': count_n})'''
        item_counts[item+'p'] = (count_p)
        item_counts[item+'n'] = (count_n)

    

    for y in Casestudy1:
            if y.processed == "Positive":
                positive_count+=1
            else:
                negative_count+=1   
    item_counts['positive'] = positive_count
    item_counts['negative'] = negative_count
    print(item_counts)
    context = item_counts
    print(context)
    '''burger = 0
    chicken = 0
    haleem = 0
    salad = 0
    mutton = 0
    others = 0
    positive = 0    
    negative = 0
    burgerp = 0
    burgern = 0
    haleemp = 0
    haleemn = 0
    chickenp = 0
    chickenn = 0
    saladp = 0
    saladn = 0
    muttonp = 0
    muttonn = 0


    sel = Casestudy.objects.filter(keywords__isnull=False)
    for data in sel:
        if 'burger' in data.keywords:
            burger+=1
            if data.processed == "Positive":
                burgerp+=1
            else:
                burgern+=1
        elif 'haleem' in data.keywords:
            haleem+=1
            if data.processed == "Positive":
                haleemp+=1
            else:
                haleemn+=1
        elif 'chicken' in data.keywords:
            chicken+=1
            if data.processed == "Positive":
                chickenp+=1
            else:
                chickenn+=1
        elif 'chicken salad' in data.keywords:
            salad+=1
            if data.processed == "Positive":
                saladp+=1
            else:
                saladn+=1
        elif 'mutton' in data.keywords:
            mutton+=1
            if data.processed == "Positive":
                muttonp+=1
            else:
                muttonn+=1
        else:
            others+=1

        if data.processed == "Positive":
            positive+=1
        else:
            negative+=1

    context = {'burger' : burger, 'haleem' : haleem, 'chicken' : chicken, 'salad' : salad, 'mutton' : mutton, 'others' : others, 'positive' : positive,
    'negative' : negative, 'burgerp' : burgerp, 'haleemp' : haleemp, 'chickenp' : chickenp, 'saladp' : saladp, 'muttonp' : muttonp, 'burgern' : burgern,
    'haleemn' : haleemn, 'chickenn' : chickenn, 'saladn' : saladn, 'muttonn' : muttonn }
    print(context)'''

    if context:
        return render(request, 'chart.html', context)
    else:
        return render(request, 'chart.html')




def chart(request):
    positive_count = 0    
    negative_count = 0
    count_p = 0
    count_n = 0
    Non = 0
    yes = 0
    item_type_list =[] 
    p_list =[] 
    n_list =[] 
    y=0
    best_list=[]
    unknown_list=[]
    xp=0
    xn=0
    items = menu.objects.values()
    Casestudy1 = Casestudy.objects.filter(keywords__isnull=False)
    item_list = [item['item_name'] for item in items]
    item_counts = {}
    for item in item_list:
        item_type = item
        item_type = 0
        count_p = 0
        count_n = 0
        for y in Casestudy1:
            if y.keywords == item:
                if y.processed == 'Positive':
                    count_p += 1
                else:
                    count_n += 1
                
        '''item_counts.append({item+'p': count_p, item+'n': count_n})'''
        item_counts[item+'p'] = (count_p)
        item_counts[item+'n'] = (count_n)
        p_list.append(count_p)
        n_list.append(count_n)
        item_type = (count_n + count_p)
        item_type_list.append(item_type)

    

    for y in Casestudy1:
        if y.processed == "Positive":
            positive_count += 1
        else:
            negative_count += 1
        if y.sarcasm == "Non-Sarcastic":
                Non+=1
        else:
                yes+=1 
        if y.keywords == 'UnKnown':
            if y.processed =='Positive':
                xp+=1
            else:
                xn+=1
        
            
    item_counts['positive'] = positive_count
    item_counts['negative'] = negative_count
    labels = [item['item_name'] for item in items]
    print(item_counts)
    best_list=labels[0]
    
    unknown_list = round((xp - xn) / (positive_count + negative_count) * 100, 2)
    context = {'labels':labels,'item_counts':item_counts,'item_type_list':item_type_list,'positive':positive_count,'negative':negative_count,'p_list':p_list,'n_list':n_list,'best_list':best_list,'unknown_list':unknown_list,'Non':Non,'yes':yes}
    print(context)
    '''burger = 0
    chicken = 0
    haleem = 0
    salad = 0
    mutton = 0
    others = 0
    positive = 0    
    negative = 0
    burgerp = 0
    burgern = 0
    haleemp = 0
    haleemn = 0
    chickenp = 0
    chickenn = 0
    saladp = 0
    saladn = 0
    muttonp = 0
    muttonn = 0


    sel = Casestudy.objects.filter(keywords__isnull=False)
    for data in sel:
        if 'burger' in data.keywords:
            burger+=1
            if data.processed == "Positive":
                burgerp+=1
            else:
                burgern+=1
        elif 'haleem' in data.keywords:
            haleem+=1
            if data.processed == "Positive":
                haleemp+=1
            else:
                haleemn+=1
        elif 'chicken' in data.keywords:
            chicken+=1
            if data.processed == "Positive":
                chickenp+=1
            else:
                chickenn+=1
        elif 'chicken salad' in data.keywords:
            salad+=1
            if data.processed == "Positive":
                saladp+=1
            else:
                saladn+=1
        elif 'mutton' in data.keywords:
            mutton+=1
            if data.processed == "Positive":
                muttonp+=1
            else:
                muttonn+=1
        else:
            others+=1

        if data.processed == "Positive":
            positive+=1
        else:
            negative+=1

    context = {'burger' : burger, 'haleem' : haleem, 'chicken' : chicken, 'salad' : salad, 'mutton' : mutton, 'others' : others, 'positive' : positive,
    'negative' : negative, 'burgerp' : burgerp, 'haleemp' : haleemp, 'chickenp' : chickenp, 'saladp' : saladp, 'muttonp' : muttonp, 'burgern' : burgern,
    'haleemn' : haleemn, 'chickenn' : chickenn, 'saladn' : saladn, 'muttonn' : muttonn }
    print(context)'''

    if context:
        return render(request, 'chart.html', context)
    else:
        return render(request, 'chart.html')