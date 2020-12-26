from django.shortcuts import render
from django import forms

from . import util

from markdown2 import Markdown

import random

markdown = Markdown()


class NewPageForm(forms.Form):
    page = forms.CharField(label="new page")
    textbody = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 70% !important; height: 50vh;'}), label="textbody")

class Search(forms.Form):
    search = forms.CharField(label="search")

class Edit(forms.Form):
    textbody = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 70% !important; height: 50vh;'}), label='')


def index(request):
    entries = util.list_entries()
    queries = []
    content = {}

    if request.method == "POST":
        queried = Search(request.POST)

        if queried.is_valid():
            query = queried.cleaned_data["search"]

            for title in entries:
                if query in entries:
                    entry = util.get_entry(query)
                    markdown_entry = markdown.convert(entry)

                    content = {
                        "title": title,
                        "entry": markdown_entry,
                        "queried": Search()
                    }

                    return render(request, "encyclopedia/entry.html", content)
                
                if query.lower() in title.lower():
                    queries.append(title)
                    content = {
                        "queries": queries,
                        "queried": Search()
                    }

            return render(request, "encyclopedia/search.html", content)

        else: 
            return render(request, "encyclopedia/index.html", {
                "queried": Search()
            })
    
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "queried": Search()
        })


def entry(request, title):
    entries = util.list_entries()
    
    if title in entries:
        entry = util.get_entry(title)
        markdown_entry = markdown.convert(entry)

        content = { 
            "title": title,
            "entry": markdown_entry,
            "queried": Search()
        }
        return render(request, "encyclopedia/entry.html", content)
    
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })


def create(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["page"]
            textbody = form.cleaned_data["textbody"]

            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {
                    "message": "The entry already exists."
                })
            
            util.save_entry(title, textbody)
            entry = util.get_entry(title)
            markdown_entry = markdown.convert(entry)

            content = {
                "title": title,
                "entry": markdown_entry
            }

            return render(request, "encyclopedia/entry.html", content)   
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewPageForm()
        })


def edit(request, title):
    if request.method == "POST":
        form = Edit(request.POST)

        if form.is_valid():
            textbody = form.cleaned_data["textbody"]
            util.save_entry(title, textbody)
            entry = util.get_entry(title)
            markdown_entry = markdown.convert(entry)

            content = {
                "queried": Search(),
                "title": title,
                "entry": markdown_entry
            }

            return render(request, "encyclopedia/entry.html", content)
    
    else:
        entry = util.get_entry(title)

        content = {
            "queried": Search(),
            "edit": Edit(initial={"textbody": entry}),
            "title": title
        }

        return render(request, "encyclopedia/edit.html", content)


def random_page(request):
    if request.method == "GET":
        entries = util.list_entries()
        title = random.choice(entries)

        entry = util.get_entry(title)
        markdown_entry = markdown.convert(entry)

        content = {
            "queried": Search(),
            "title": title,
            "entry": markdown_entry
        }

        return render(request, "encyclopedia/entry.html", content)
