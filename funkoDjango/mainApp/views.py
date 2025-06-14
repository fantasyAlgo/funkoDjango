from asyncio import wait
from django.shortcuts import render, HttpResponse
from .models import FunkoPop, Review, User
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import F

def home(request):
    funkos = FunkoPop.objects.all()
    return render(request, "home.html", {"funkos" : funkos} )

def shop(request):
    funkos = FunkoPop.objects.all()
    if "search" in request.GET:
        search = request.GET.get("search")
        funkos = funkos.filter(name=search)

    if "category" in request.GET:
        cat = request.GET.get("category")
        funkos = funkos.filter(category = cat)
    if "price" in request.GET:
        priceRange = request.GET.get("price").split("-")
        if priceRange[0] == "50+":
            funkos = funkos.filter(cost__range=(50, 1000))
        else:
            funkos = funkos.filter(cost__range=(int(priceRange[0]), int(priceRange[1])))

    if len(funkos) == 0:
        return render(request, "shop.html", {"funkos" : [], "it" : 1})


    try:
        it = int(request.GET.get("it"))
        return render(request, "shop.html", {"funkos" : funkos[50*(it-1):50*it], "it" : it} )
    except:
        return render(request, "shop.html", {"funkos" : funkos[:50], "it" : 1})

def item(request):
    try:
        id = int(request.GET.get("item"))
    except:
        return redirect("/shop")
    funko = FunkoPop.objects.get(id=id)
    related_funkos = FunkoPop.objects.filter(category=funko.category)
    reviews = Review.objects.filter(item=funko)
    sizeReviews = len(reviews)
    average_rating = round(sum([ r.stars for r in reviews])/sizeReviews, 2)
    perc_stars = [0,0,0,0,0,0]
    for r in reviews:
        perc_stars[r.stars] += 1.0
    for i in range(6):
        perc_stars[i] /= sizeReviews/100
        perc_stars[i] = round(perc_stars[i], 2)

    return render(request, "item.html", {"funko" : funko, 
                                         "related_funkos" : related_funkos[:4], 
                                         "reviews" : reviews, 
                                         "average_rating" : average_rating, 
                                         "perc_1stars" : perc_stars[1],
                                         "perc_2stars" : perc_stars[2],
                                         "perc_3stars" : perc_stars[3],
                                         "perc_4stars" : perc_stars[4],
                                         "perc_5stars" : perc_stars[5]})

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.filter(email=email).first()
        if user == None:
            return HttpResponse("No user")
        is_valid = check_password(password, user.password)
        print(email,password)
        if is_valid:
            request.session['username'] = user.username
            return redirect("/")
        else:
            return redirect("/login")

    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("confirm_password")
        if password != password2:
            return HttpResponseBadRequest("Invalid input")
        hashed_password = make_password(password)
        User.objects.create(username=username, email=email, password=hashed_password)
        return redirect('/login')
    else:
        return render(request, "login.html")



def add_to_cart(request, product_id):
    if 'username' not in request.session:
        return redirect("/login")
    user = User.objects.filter(username=request.session.get("username")).first()
    funko = FunkoPop.objects.filter(id=product_id).first()

    if user == None or funko == None:
        return redirect("/login")
    user.funkos.add(funko)
    return redirect("/shop")

def remove_from_cart(request):
    if 'username' not in request.session:
        return redirect("/login")
    user = User.objects.filter(username=request.session.get("username")).first()
    id = request.GET.get("id")
    funko = FunkoPop.objects.filter(id=id).first()
    user.funkos.remove(funko)
    return redirect("/orders")
def remove_from_wishlist(request):
    if 'username' not in request.session:
        return redirect("/login")
    user = User.objects.filter(username=request.session.get("username")).first()
    id = request.GET.get("id")
    funko = FunkoPop.objects.filter(id=id).first()
    user.wishedFunkos.remove(funko)
    return redirect("/orders")




def orders(request):
    if 'username' not in request.session:
        return redirect("/login")
    user = User.objects.filter(username=request.session.get("username")).first()
    funkos = user.funkos.all()
    totalCost = 0
    for f in funkos:
        totalCost += f.cost
    return render(request, "cart.html", {"cart_items" : funkos, "subtotal" : totalCost, "total" : totalCost+9.5})

def wishlist(request):
    if 'username' not in request.session:
        return redirect("/login")
    user = User.objects.filter(username=request.session.get("username")).first()
    funkos = user.wishedFunkos.all()
    totalCost = sum([f.cost for f in funkos])
    return render(request, "wishlist.html", {"wishlist_items" : funkos, "subtotal" : totalCost})

def logout(request):
    request.session.pop('username', None)
    return redirect("/login")

def payment(request):
    if 'username' not in request.session:
        return redirect("/login")
    user = User.objects.filter(username=request.session.get("username")).first()
    funkos = user.funkos.all()
    return render(request, "payment.html", {"cart_items" : funkos})

def clear_cart(request):
    if 'username' not in request.session:
        return redirect("/login")
    user = User.objects.filter(username=request.session.get("username")).first()
    user.funkos.clear()
    return redirect("/")

def add_review(request, funko_id):
    if 'username' not in request.session:
        return redirect("/login")
    user = User.objects.filter(username=request.session.get("username")).first()
    funko = FunkoPop.objects.get(id=funko_id)
    title =       request.POST.get("title")
    description = request.POST.get("description")
    stars =       request.POST.get("rating")
    Review.objects.create(title=title,description=description, stars=stars, user=user, item=funko)
    return redirect(f"/item?item={funko_id}")

def add_to_wishlist(request):
    if 'username' not in request.session:
        return redirect("/login")
    product_id = request.GET.get("product_id")
    user = User.objects.filter(username=request.session.get("username")).first()
    funko = FunkoPop.objects.filter(id=product_id).first()

    if user == None or funko == None:
        return redirect("/login")
    user.wishedFunkos.add(funko)
    return JsonResponse({'status': 'success', 'product_id': product_id})




