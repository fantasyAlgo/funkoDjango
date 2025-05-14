from asyncio import wait
from django.shortcuts import render, HttpResponse
from .models import FunkoPop, Review, User
from django.http import HttpResponseBadRequest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect

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
    return render(request, "item.html", {"funko" : funko, "related_funkos" : related_funkos[:4], "reviews" : reviews})

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



def orders(request):
    if 'username' not in request.session:
        return redirect("/login")
    user = User.objects.filter(username=request.session.get("username")).first()
    funkos = user.funkos.all()
    totalCost = 0
    for f in funkos:
        totalCost += f.cost
    return render(request, "cart.html", {"cart_items" : funkos, "subtotal" : totalCost, "total" : totalCost+9.5})


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

