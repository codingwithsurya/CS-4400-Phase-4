# CS-4400-Phase-4
cs 4400 phase 4 project shared github

https://docs.google.com/document/d/1633UA-v3UTln1s15PQil72YFTob3CcfW-uWh_LKw8yI/edit?usp=sharing


### Start Server
``` python manage.py runserver ```

### Setup DB Initially
```python manage.py inspectdb > models.py```

### Check which Apps are installed in settings
```python manage.py shell -c "from django.conf import settings; print(settings.INSTALLED_APPS)"```

## Current Admin Password
* Username: cs4400
* Password: databasecourse

## View Urls
* /alternative-airport/
* /flights-in-the-air/
* /flights-on-the-ground/
* /people-in-the-air/
* /people-on-the-ground/
* /route-summary/
