from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util
import random
import markdown2

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8', 'maxlength':30, 'required' : True}))
    content = forms.CharField(label="Entry content", widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10, 'maxlength':1000, 'required' : True}))

class EditEntryForm(forms.Form):
    content = forms.CharField(label="Entry content", widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10, 'maxlength':1000, 'required' : True}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, title):
    try:
        return render(request, "encyclopedia/entry.html", {
            "entry":markdown2.markdown(util.get_entry(title)),
            "title":title
        })
    except:
        return render(request, "encyclopedia/error.html", {
            "title":title,
            "error":1
        })

def get_random(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("encyclopedia:get_entry", kwargs={'title': title }))

def get_search(request):
    value = request.GET.get('q','')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("encyclopedia:get_entry", kwargs={'title': value }))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringEntries.append(entry)

        return render(request, "encyclopedia/search.html", {
        "entries": subStringEntries,
        "value": value
    })

def newEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            upperlist = [x.upper() for x in util.list_entries()]
            if title.upper() in upperlist:
                return render(request, "encyclopedia/error.html",{
                    "title":title,
                    "error":2
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            return render(request, "encyclopedia/newPage.html", {
                "form":form
            })

    return render(request, "encyclopedia/newPage.html", {
        "form": NewEntryForm()
    })

def editEntry(request, title):
    if request.method =="POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            return render(request, "encyclopedia/error.html",{
                    "title":title,
                    "error":3
                })

    return render(request, "encyclopedia/edit.html", {
        "form": EditEntryForm(initial={'content': util.get_entry(title)}),
        "title": title,
    })