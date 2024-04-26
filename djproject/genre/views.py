from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Collection, Piece
from .forms import UserForm
from django.contrib.auth import authenticate, login
from django.views.generic import View
# Create your views here.

def index(request):
    all_collection=Collection.objects.all()
    context = {  
        "all_collection":all_collection,
    }
    return render(request,"genre\\index.html", context)


def details(request, genre_id):
    Citem=Collection.objects.get(pk=genre_id)
    Pitem=Piece.objects.filter(collection=Citem)
    context ={
        "Pitem":Pitem,
    }
    return render(request,"genre\\details.html",context)

class UserFormView(View):
    form_class=UserForm
    template_name="genre\\signing.html"

    def get(self,request):
        form=self.form_class(None)
        return render (request,self.template_name,{'form':form})
    
    def post(self,request):
        form=self.form_class(request.POST)

        if form.is_valid():
            user=form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()

            newuser=authenticate(username=username,password=password)

            if newuser is not None:
                if newuser.is_active:
                    login(request,newuser)
                    return redirect("/genres")

        return render(request,self.template_name,{'form':form})

