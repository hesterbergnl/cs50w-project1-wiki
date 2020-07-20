from django.shortcuts import render
from . import util
import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class NewArticleForm(forms.Form):
	title = forms.CharField(label="Title")
	body =  forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}), label="Body (markdown)")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
	return render(request, "encyclopedia/wiki.html", {
			"title": title,
			"entry": markdown2.markdown(util.get_entry(title))
		})

def add(request, title=""):
	if request.method == "POST":
		form = NewArticleForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			body = form.cleaned_data["body"]
			util.save_entry(title, body)
			return HttpResponseRedirect(reverse("encyclopedia:index"))
		else:
			return render(request, "add.html", {
					"form": form
				})
	else:
		return render(request, "encyclopedia/add.html", {
				"form": NewArticleForm(initial={'title': title, 'body': body})
			})

def search(request):
	query = request.GET['q']
	entry = util.get_entry(query)
	if entry != None:
		return HttpResponseRedirect(reverse("encyclopedia:wiki" , args=[query]))
	else:
		search_results = util.find_substrings(query)
		return render(request, "encyclopedia/search.html", {
				"query": query,
				"results": search_results
			})

def edit(request, title):
	body = util.get_entry(title)
	return render(request, "encyclopedia/add.html", {
				"form": NewArticleForm(initial={'title': title, 'body': body})
			})

def random(request):
	title = util.random_page()
	return render(request, "encyclopedia/wiki.html", {
			"title": title,
			"entry": markdown2.markdown(util.get_entry(title))
		})