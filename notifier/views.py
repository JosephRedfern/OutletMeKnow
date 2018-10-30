from django.shortcuts import render, redirect
from .models import OutletModel, NotificationRequest
from .forms import NotificationRequestForm
from django.http import HttpResponseRedirect, HttpResponse


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
            model = form.cleaned_data['model']

            nr = NotificationRequest()
            nr.email = email
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
    return render(request, 'notifier/show_all.html', context)


def status(request):
    context = {}
    models = OutletModel.objects.all().order_by('last_checked')
    context['products'] = models

    return render(request, 'notifier/status.html', context)


def thanks(request):
    return render(request, 'notifier/thanks.html', {})


def visit(request, uuid):
    nr = NotificationRequest.objects.filter(uuid=uuid).first()
    nr.visited += 1
    nr.save()

    print("NOW: {}".format(nr.visited))

    # return HttpResponse("dfg")
    return redirect(nr.model.url)


def inventory_details(request, mid):
    context = {}
    model = OutletModel.objects.get(id=mid)

    context['model'] = model
    return render(request, 'notifier/inventory_details.html', context)
