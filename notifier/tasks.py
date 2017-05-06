# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import os
import requests
import re
from datetime import datetime
from notifier.models import OutletModel, StockHistory, NotificationRequest
from twilio.rest import Client
from .credentials import *
@shared_task
def check_stock():
    for om in OutletModel.objects.all():
        resp = requests.get(om.url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'})
        parsed = re.findall("(\d+) in stock", resp.text)
        total = sum([int(x) for x in parsed])

        entry = StockHistory()
        entry.stock_count = total
        entry.response = resp.text
        entry.model = om
        entry.save()

        print("{}:{}".format(om.name, total))


@shared_task
def process_notifications():
    unprocessed = NotificationRequest.objects.filter(sent__isnull=True)
    twilio_client = Client(TWILIO_ACCOUNT, TWILIO_TOKEN)

    for nr in unprocessed:
        if nr.model.get_stock_count().stock_count > 0:
            model_count = nr.model.get_stock_count().stock_count
            model_name = nr.model.name

            nr.sent = datetime.now()
            nr.save()

            if nr.email is not None:
                print("Sending Email!")
                requests.post(
                    "https://api.mailgun.net/v3/mg.redfern.me/messages",
                    auth=("api", MAILGUN_KEY),
                    data={
                        "from": "Outlet Notifier <joseph@redfern.me>",
                        "to": "Joseph Redfern <joseph@redfern.me>",
                        "subject": "OutletMeKnow: {} stock update".format(model_name),
                        "text": "There {} now {} {}'s in stock. Buy at: http://outletmeknow.redfern.me/notification/{}".format("are" if model_count > 1 else "is", model_count, model_name, nr.uuid)})

            if nr.mobile_number is not None:
                msg = "There are now {} {}'s in stock. Buy at: http://outletmeknow.redfern.me/notification/{}".format(model_count, model_name, nr.uuid)
                print("Sending message: {}".format(msg))
                twilio_client.messages.create(to=nr.mobile_number, from_="+442825022666", body=msg)

        else:
            print("No stock for {}".format(nr.model.name))