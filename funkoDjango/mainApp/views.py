from django.shortcuts import render, HttpResponse
from .models import FunkoPop

def home(request):
    funkos = FunkoPop.objects.all()
    return render(request, "home.html", {"funkos" : funkos} )

def shop(request):
    funkos = FunkoPop.objects.all()
    # Selection part
    try:
        cat = request.GET.get("category")
        priceRange = request.GET.get("price")
        sort = request.GET.get("sort")
        print("category: ", cat)
        if cat != None and cat != "Other":
            funkos = FunkoPop.objects.filter(category = cat)
    except:
        pass
    if len(funkos) == 0:
        return render(request, "shop.html", {"funkos" : [], "it" : 1})

    print(funkos[0].description, funkos[0].id)

    try:
        it = int(request.GET.get("it"))
        return render(request, "shop.html", {"funkos" : funkos[50*(it-1):50*it], "it" : it} )
    except:
        return render(request, "shop.html", {"funkos" : funkos[:50], "it" : 1})

def item(request):
    id = int(request.GET.get("item"))
    funko = FunkoPop.objects.get(id=id)
    related_funkos = FunkoPop.objects.filter(category=funko.category)
    return render(request, "item.html", {"funko" : funko, "related_funkos" : related_funkos[:4]} )




