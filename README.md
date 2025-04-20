# CS-4400-Phase-4
cs 4400 phase 4 project shared github

https://docs.google.com/document/d/1633UA-v3UTln1s15PQil72YFTob3CcfW-uWh_LKw8yI/edit?usp=sharing

### Testing front end setup to check stored procedures
https://www.youtube.com/watch?v=eXrwF4LXF5c
* On minute 9 currently


### Environment setup
```pip install django djangorestframework django-cors-headers```
### Start Server
``` python manage.py runserver ```

### Run migrations in case run into errors
```python manage.py makemigrations;```
```python manage.py migrate;```

### Setup DB Initially
```python manage.py inspectdb > models.py```

### If you want to run the frontend 
```cd frontendFlights```
```npm run dev```

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
