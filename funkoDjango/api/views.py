
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import FunkoPopSerializer
from mainApp.models import FunkoPop

@api_view(["GET"])
def getAllFunkos(request):
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
    serializer = FunkoPopSerializer(funkos, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getItem(request):
    try:
        id = int(request.GET.get("item"))
        funko = FunkoPop.objects.get(id=id)
        serializer = FunkoPopSerializer([funko], many=True)
        #print("chill", funko.name)
        return Response(serializer.data)
    except:
        return Response([])


    

