from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

# Create your views here.

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        realtor_email = request.POST['realtor_email']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        user_id = request.POST['user_id']
        message = request.POST['message']
        if request.user.is_authenticated:
            user_id = request.POST['user_id']
            has_contacted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(request,'You have already make an enquiry! Please wait for the response')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing_id=listing_id,listing=listing,name=name,email=email,user_id=user_id,message=message,phone=phone)
        contact.save()

        #mail
        send_mail(
            'Property listing Inquiry',
            'There has been an inquiry for' +listing + '.sign in for more info',
            'anirudhmittal1117@gmail.com',
            [realtor_email,'anirudh.16bcs1117@gmail.com'],
            fail_silently=True
        )

        messages.success(request,'Your inquiry succcesfully submitted')
    return redirect('/listings/'+listing_id)
