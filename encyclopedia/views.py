import random
from django.shortcuts import render, redirect
import markdown
from . import util


def index(request):
    count = util.list_entries()
    count = len(count)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "count": count
    })

# function of displaying pages if it exist with calling the convert function
def user_entry(request, title):
    entries_content = util.get_entry(title)
    # here im compering between my entry data if user input not exist or none
    if entries_content == None:
        # it will render error page
        return render(request, "encyclopedia/error_404.html", {
            "massage": "This page not found",
            "title": title
        })
    # else it will render the title page
    else:
        entries_content = markdown.markdown(entries_content)
        # convert the entries and return
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": entries_content
        })

# search bar function for showing the result
def find(request):
    # here i getting  the data from the user with get method
    if request.method == 'GET':
        input = request.GET.get('q')
        available = markdown.markdown(input)
        all_data = util.list_entries()
        sugg_results = []
        # for loop to transform the input in lower case
        for entry in all_data:
            if input.lower() in entry.lower():
                sugg_results.append(entry)
                # for loop to compare if the entered title is available or no
        for entry in all_data:
            # if the user input in my entry return it
            if input.lower() == entry.lower():
                return render(request, "encyclopedia/entry.html", {
                    "entry": available,
                    "title": input
                })
            # here an empty list to suggest if the user enter any letter in my titles
            elif sugg_results != []:
                # show my how may article with user input letter
                count = len(sugg_results)
                return render(request,  "encyclopedia/suggest.html", {
                    "sugg_results": sugg_results,
                    "count": count
                })
            else:
                # else return 404 page with massage inform user that we don't have this title
                return render(request, "encyclopedia/error_404.html", {
                    "massage": "This Title of article Not Available",
                    "title": input
                })
# function that for the new page and made it to receive  a article input


def add_article(request):
    # if user want to create a a new page return new article page with get method
    if request.method == "GET":
        return render(request, "encyclopedia/new_article.html")
    else:
        # here im using post method to push the title and content as a new md fils
        title = request.POST['title']
        content = request.POST['content']
        title_exist = util.get_entry(title)
        # taking the user input and compare title with my data if the user title already exist
        if title_exist != None:
            # return 404 page
            return render(request, "encyclopedia/error_404.html", {
                "massage": "this Article is already Exists or you entered empty Article",
                'title': title
            })
        # if no we will save the user input with save function and return the last article page
        else:
            util.save_entry(title, content)
            entries_content = markdown.markdown(title)
            return render(request,"encyclopedia/entry.html", {
                "title": title,
                "content": entries_content
            })

# creating a edit button for editing article
def edit_page(request):
    # if the request is getting
    if request.method == 'GET':
        #get the title with content
        title = request.GET['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content
        })
    # post method for publishing the new editing of the content and title
    if request.method == "POST":
        #if request is posting post the new title and content
        title = request.POST['title']
        content = request.POST['content']
        # using save function for updating last editing
        util.save_entry(title, content)
        # convert last editing from md to html and display it
        entries_content = markdown.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": entries_content
        })
# function for random page
def random_page(request):
    content = util.list_entries()
    title = random.choice(content)
    return redirect("user_entry", title)


