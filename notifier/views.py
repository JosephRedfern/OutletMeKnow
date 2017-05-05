from django.shortcuts import render
from .models import OutletModel, NotificationRequest
from .forms import NotificationRequestForm
from django.http import HttpResponseRedirect


def request_notification(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NotificationRequestForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            email = form.cleaned_data['email_address']
            mobile = form.cleaned_data['mobile_number']
            model = form.cleaned_data['model']

            nr = NotificationRequest()
            nr.email = email
            nr.mobile_number = mobile
            nr.model = model
            nr.save()


            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NotificationRequestForm()

    return render(request, 'notifier/request_notification.html', {'form': form})

def show_all(request):
    context = {}
    context['models'] = OutletModel.objects.all()
    print(context['models'])
    return render(request, 'notifier/show_all.html', context)

def thanks(request):
    return render(request, 'notifier/thanks.html', {})