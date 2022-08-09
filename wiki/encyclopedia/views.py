from audioop import reverse
from random import randrange
from django.http import HttpResponse
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from . import util
from django.contrib import messages
import markdown2

class NewPageForm(forms.Form):
    # i want the user to provide the name of the page
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control mb-4",
                "placeholder": "Content.."}))

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control mb-4",
                "placeholder": "Content.."}))
                
def newPage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data.get("content")
            # page already exists
            entries = util.list_entries()
            for entry in entries:
                if title.lower() == entry.lower():
                    messages.error(request,"Title already exists..") 
                    return render(request, "encyclopedia/new_page.html", {
                    "form": form
                })
            util.save_entry(title,content)
            return redirect("entry", title)
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })
    # request method == GET 
    return render(request, "encyclopedia/new_page.html", {
      "form" : NewPageForm()
    })

def index(request):
    return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
    })



def search(request):
    # The request object contains information about the user's request. What data they've sent to the page, where they are coming from, etc.
    # request.GET is the dictionary of the GET variables in the http request made to your server for example:
    # http://127.0.0.1:8000/wiki/q=Python
    # request.GET would be: {"q": Python}
    # Because request.GET is a dictionary, it has the method .get() which retrieves a value for a key in the dictionary
    query = request.GET.get("q", "")

    if query is None or query == "":
        return render(
            # passing the found_entries variable as an empty string and the query to the search results template so they can be displayed
            request,
            "encyclopedia/search_results.html",
            {"found_entries": "", "query": query},
        )

    entries = util.list_entries()

    # declaring a list with all the valid entries found (comparing the lowercase query to lowercase entries)
    found_entries = [
        valid_entry
        for valid_entry in entries
        # if String Contains Substring
        if query.lower() in valid_entry.lower()
    ]
    # the list contains one matching entry
    if len(found_entries) == 1:
        return redirect("entry", found_entries[0])
    return render(
        request,
        "encyclopedia/search_results.html",
        {"found_entries": found_entries, "query": query},
    )
def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get("content")
            util.save_entry(title, content)
            return redirect("entry", title)
    entry = title
    content = util.get_entry(entry)
    form = EditForm({"content":content})
    return render(request, "encyclopedia/edit.html", {
            "title" : entry,
            "form": form
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html" , {
        "title" : title,
         "entry" : markdown2.markdown(util.get_entry(title))
         })
         
def random(request):
    entries = util.list_entries()
    num = randrange(0, len(entries))
    return entry(request, entries[num])