from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList


def index(request, page_id):
    ls = ToDoList.objects.get(id=page_id)

    # if the list (ls) is in the users lists
    if ls in request.user.todolist.all():
        # the template (html file) passes a dictionary to this function with the information regarding buttons, checkboxes, etc.
        # i.e. {"save":["save"], "c1":["clicked"]}
        if request.method == "POST":
            print(request.POST)
            if request.POST.get("save"):             # put name of button in the quotes
                for item in ls.item_set.all():
                    if request.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    
                    item.save()

            elif request.POST.get("newItem"):
                txt = request.POST.get("new")

                # this bool finds if any existing items match new (txt). only allows unique item names in list
                isNotInList = len(ls.item_set.filter(text=txt)) == 0

                if len(txt) > 2 and isNotInList:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("invalid input")

        return render(request, "main/list.html", {"ls": ls})
    return render(request,"main/view.html", {})


def home(request):
    return render(request, "main/home.html", {})


def create(request):
    if request.method == "POST":
        form = CreateNewList(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            request.user.todolist.add(t)

        return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()
    return render(request, "main/create.html", {"form": form})

def view(request):
    return render(request, "main/view.html", {})