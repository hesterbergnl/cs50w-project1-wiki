from django.shortcuts import render

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
	return render(request, "encyclopedia/wiki.html", {
			"title": title,
			"entry": markdown2.markdown(util.get_entry(title))
		})