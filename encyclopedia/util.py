import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from random import randint


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def find_substrings(search_term):
    """
    Retreives article titles that the search is a substring of
    """
    entries = list_entries()
    search_results = []
    for entry in entries:
        if search_term in entry:
            search_results.append(entry)

    return search_results

def random_page():
    """
    Finds a random number between 0 and the length of the entries list
    Returns the name of a random article
    """
    entries = list_entries()
    random_number = randint(0, len(entries) - 1)
    return entries[random_number]