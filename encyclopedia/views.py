from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from . import util
from .util import get_entry, list_entries, save_entry, Create_wiki, Edit_existing_wiki
import random 
import markdown2

def index(request):
    try:
        q = request.GET['q']
        print(q)
        content = get_entry(q)
        if content == None:
            entries = list_entries()
            search_results = []
            print(entries)

            for entry in entries:
                if entry.find(q) >= 0:
                    search_results.append(entry)

            if len(search_results) == 0:
                return render(request, "encyclopedia/error.html", {
                    "title": f"{q} not found",
                    "content": "google it you idiot."
                })
            else:
                return render(request, "encyclopedia/search.html", {
                    "entries": search_results,
                    "keyword": q
                })

        else:
            return render(request, "encyclopedia/entry.html", {
                "title": q,
                "content": content
            })            
    except:
        return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })


def wiki(request, title):
    try:
        content = get_entry(title)
        print(content)
    except:
        return render(request, "encyclopedia/error.html", {
            "title": f"{title} not found",
            "content": "404 Not Found"
        })


    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content)
    })

def new_wiki(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new_wiki.html" ,{
            "form": Create_wiki()
        })
    else:
        form = Create_wiki(request.POST)
        if form.is_valid():
            if form.cleaned_data['title'] not in list_entries():
                save_entry(form.cleaned_data['title'], form.cleaned_data['content'])
                return render(request, "encyclopedia/entry.html", {
                    "title": form.cleaned_data['title'],
                    "content": markdown2.markdown(form.cleaned_data['content'])
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "title": f"{form.cleaned_data['title']} already exist",
                    "content": "please try again"
                })
        else:
            return render(request, "encyclopedia/new_wiki.html" ,{
                "form": Create_wiki()
            })

def random_entry(request):
    entries = list_entries()
    n = random.randint(0, len(entries)-1)
    print(n)
    content = get_entry(entries[n])
    return render(request, "encyclopedia/entry.html", {
        "title": entries[n],
        "content": markdown2.markdown(content)
    })

def edit_wiki(request, title):
    if request.method == 'GET':
        old_content = get_entry(title)
        return render(request, "encyclopedia/edit_entry.html", {
            "title": title,
            "old_content": old_content,
            "form": Edit_existing_wiki()
        })
    else:
        form = Edit_existing_wiki(request.POST)
        if form.is_valid():
            save_entry(title, form.cleaned_data['new_content'])
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": markdown2.markdown(form.cleaned_data['new_content'])
            })

        else:
            return render(request, "encyclopedia/new_wiki.html" ,{
                "form": Create_wiki()
            })

