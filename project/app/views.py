from django.shortcuts import render,redirect
from.models import*
from django.contrib.auth.models import auth,User
from django.template.loader import render_to_string
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth import logout
from django.http import HttpResponse

import numpy as np
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
import pickle



df=pd.read_csv('new_cleaned_data.csv', index_col=0)

texts = df['new_text'].astype(str)
y = df['is_offensive']

vectorizer = CountVectorizer(stop_words='english', min_df=0.0001)
X = vectorizer.fit_transform(texts)

loaded_model = pickle.load(open("svm_model.pkl", 'rb'))



# Create your views here.


# def home(request):
#     return render(request,'home.html')


def register(request):
    if request.method=="POST":
        username=request.POST['uname']
        email=request.POST['mail']
        password1=request.POST['p_password']
        password2=request.POST['pp_password']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                 print("hai")
                 return render(request,'reg_form.html',{'key':'Username already taken'})
            elif User.objects.filter(email=email).exists():
                print("hello")
                return render(request,'reg_form.html',{'key':'email already taken'})
            else:
                user=User.objects.create_user(username=username,password=password1,email=email)
                user.save()

                
                print("saved")
                return redirect(login)
        else:
            return render(request,'reg_form.html',{'key':'Password does not match'})
    return render(request,'reg_form.html')
            




   


def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        
        userr=auth.authenticate(username=username,password=password)
        if userr is not None:
            auth.login(request,userr)
            print("login success")

            return redirect(welcome)
        else:
            
            return render(request,'login_form.html',{'key':'Invalid User'})
    return render(request,'login_form.html')


@login_required
def welcome(request):
    b=request.user
    a=imag.objects.all().order_by('-id')
    if request.method=='POST':
        post_id=request.POST['post_pk']
        post_comment=request.POST['comment']
        post = imag.objects.get(id=post_id)
        comment(img=post,user=request.user,comment=post_comment).save()
    return render(request,'welcome.html',{'key':a,'key1':b})


@login_required
def upload_img(request):
    b=request.user
    user=User.objects.get(username=request.user)
    a=imag.objects.filter(user__id=request.user.id).order_by('-id')
    
    if request.method=="POST":
        im=request.FILES['imagee']
        imag(user=user,image=im).save()

        a=imag.objects.filter(user__id=request.user.id).order_by('-id')
        print(len(a))
        #return render(request,'uploadimg.html',{'views':a,'view1':b})
        return redirect(upload_img)
    return render(request,'uploadimg.html',{'views':a,'view1':b})

# def upload_img(request):
#     if imag.objects.get(user=request.u):
#         a=imag.objects.get(user=request.u)
#         di={'views':a}
#         return render(request,'uploadimg.html',di)
#     return render(request,'uploadimg.html')

@login_required
def delete(request,pk):
    a=imag.objects.filter(id=pk)
    a.delete()
    return redirect(upload_img)

@login_required
def view_comments(request):
    pk = request.GET.get('id')
    print(pk)
    template_name = 'comments.html'
    instances = comment.objects.filter(img__pk=pk)
    if instances :  
        context = {
            'comments' : instances,
        }
        html_content = render_to_string(template_name,context)
        print(html_content)
        response_data = {
            "status" : "true",
            'template' : html_content,
        }
    else:
        response_data = {
            "status" : "false",
            "message" : "Product not found"
        }
    
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')



@login_required
def logout1(request):
    logout(request)
    return redirect(login)

def detect(request,pk):
    com=comment.objects.get(id=pk)
    d=vectorizer.transform([com.comment])
    ans=loaded_model.predict(d)
    if ans[0]==0:

       # return HttpResponse("Non-Bullying")
       return render(request,'output.html',{'k':'Non bullying'})
    else:
        #return HttpResponse("Bullying")
        return render(request,'output.html',{'k':'Bullying'})

