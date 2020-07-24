from django.shortcuts import render
from . import util
import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

#New Article Form
#Contains a edit_mode field for validation if the article exists
class NewArticleForm(forms.Form):
	title = forms.CharField(label="Title")
	body =  forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}), label="Body (markdown)")
	edit_mode = forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False)

	#https://stackoverflow.com/questions/30227119/extending-form-is-valid
	def clean(self):
		cleaned_data = self.cleaned_data
		title = cleaned_data.get("title")
		body = cleaned_data.get("body")
		edit_mode = cleaned_data.get("edit_mode")
		#https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
		if(not edit_mode and util.get_entry(title) != None):
			raise forms.ValidationError('Invalid title - article already exists')

		return cleaned_data

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
	raw_markdown = util.get_entry(title)
	if(raw_markdown == None):
		return render(request, "encyclopedia/page_not_found.html")
	else:
		return render(request, "encyclopedia/wiki.html", {
				"title": title,
				"entry": markdown2.markdown(raw_markdown)
			})

def add(request):
	if request.method == "POST":
		form = NewArticleForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			body = form.cleaned_data["body"]
			
			util.save_entry(title, body)
			return HttpResponseRedirect(reverse("encyclopedia:wiki" , args=[title]))
		else:
			return render(request, "encyclopedia/add.html", {
					"form": form
				})
	else:
		return render(request, "encyclopedia/add.html", {
				"form": NewArticleForm()
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
				"form": NewArticleForm(initial={'title': title, 'body': body, 'edit_mode': True})
			})

def random(request):
	title = util.random_page()
	return HttpResponseRedirect(reverse("encyclopedia:wiki" , args=[title]))
	
'''	return render(request, "encyclopedia/wiki.html", {
			"title": title,
			"entry": markdown2.markdown(util.get_entry(title))
		})'''