# OutletMeKnow
This webapp allows people to subscribe to notifications about Dell Outlet stock updates.

It's written in Python (with Django), and uses Celery for task management.

At the moment, it has a dependency on PostgreSQL due to the use of LEAD and LAG, althoough these can likely easily be removed.

To deploy, install dependencies (`pip install -r requirements.txt`), start celery queue workers (`celery -A OutletMeKnow worker -l info -S django` and `celery -A OutletMeKnow beat -l info -S django`).

You also need to specify your Mailgun and Twilio tokens in [credentials.py](https://github.com/JosephRedfern/OutletMeKnow/blob/master/notifier/credentials.py). It should be farily trivial to add support for additional providers.(see https://github.com/JosephRedfern/OutletMeKnow/blob/master/notifier/tasks.py#L39).
