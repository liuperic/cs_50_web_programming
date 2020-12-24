from django.shortcuts import render
from django import forms

from . import util

from markdown2 import Markdown

markdown = Markdown()


class NewPageForm(forms.Form):
    page = forms.CharField(label="new page")
    textbody = forms.CharField(widget=forms.Textarea(), label="textbody")

class Search(forms.Form):
    search = forms.CharField(label="search")


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


