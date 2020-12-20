from django.shortcuts import render
from django import forms

from . import util

from markdown2 import Markdown

mark_down = Markdown()


class NewPageForm(forms.Form):
    page = forms.CharField(label="New Page")
    textbody = forms.CharField(widget=forms.Textarea(), label="textbody")


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entries = util.list_entries()
    
    if title in entries:
        entry = util.get_entry(title)
        markdown_entry = mark_down.convert(entry)

        content = { 
            "title": title,
            "entry": markdown_entry
        }
        return render(request, "encyclopedia/entry.html", content)
    
    else:
        return render(request, "encyclopedia/error.html")
