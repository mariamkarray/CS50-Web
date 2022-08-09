from audioop import reverse
from django.http import HttpResponse
from django import forms
import markdown
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from . import util
def index(request):
    return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
    })
def entry(request, title):
    return HttpResponse (markdown.markdown(util.get_entry(title)))
    
def search(request):
    query = request.GET.get("q", "")
    if query is None or query == "":
        return render(
            request,
            "encyclopedia/search_results.html",
            {"found_entries": "", "query": query},
        )

    entries = util.list_entries()

    found_entries = [
        valid_entry
        for valid_entry in entries
        if query.lower() in valid_entry.lower()
    ]
    if len(found_entries) == 1:
        return redirect("entry", found_entries[0])

    return render(
        request,
        "encyclopedia/search_results.html",
        {"found_entries": found_entries, "query": query},
    )
