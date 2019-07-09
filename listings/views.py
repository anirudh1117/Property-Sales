from django.shortcuts import render, get_object_or_404
from .models import Listing
from realtors.models import Realtor
from .choices import bedroom_choices,price_choices,state_choices
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings,3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings':paged_listings
    }

    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing,pk=listing_id)
    mvp_realtor = Realtor.objects.all().filter(is_mvp=True)
    context = {
        'listing':listing,
        'mvp_realtor' :mvp_realtor
    }
    return render(request, 'listings/listing.html',context)

def search(request):
    query_set =Listing.objects.order_by('-list_date')

    #keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            query_set = query_set.filter(description__icontains=keywords)
  
    #city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            query_set = query_set.filter(city__iexact=city)

    #state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            query_set = query_set.filter(state__iexact=state)
    
    #bedrooms
    if 'bedrooms' in request.GET:
        bedroom = request.GET['bedrooms']
        if bedroom:
            query_set = query_set.filter(bedroom__gte=bedroom)

    #prices
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            query_set = query_set.filter(price__lte=price)

    context = {
        'bedroom_choices':bedroom_choices,
        'price_choices':price_choices,
        'state_choices':state_choices,
        'listings':query_set,
        'values':request.GET       
    }
    return render(request, 'listings/search.html',context)
