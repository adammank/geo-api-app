# Geo Api Application
Adam Mańk

## Table of contents
1. Preface  
2. Deployment
3. Auth endpoints
4. Geo Address endpoints
5. Prerequisites for setting it locally
6. Setup
7. Debugging
8. Packages used

___
### 1. Preface
        API is able to store geolocation data in the database, based on the passed IP
    address or URL. It connects with the external API to obtain and verify the geolocation data.

        API is secured by JWT token, which means that without sending apropriate
    header, you do not have an access to the endpoints.
    
        You can create an account on the /register/ endpoint and then obtain the tokens
    on the /token/ endpoint.

___
### 2. Deployment
You can use this Geo Api Application under the following url:  

    https://geo-api-app.herokuapp.com/

___
### 3. Auth endpoints
Create an account and then obatin tokens.

    /user/register/        POST        Create a user.
                                        {"username": "...", 
                                         "password": "...", "password2": "..."}

    /user/token/           POST        Obtain tokens for a user.
                                        {"username": "...", "password": "..."}
    
    /user/token/refresh/   POST        Obtain a new access token (lifetime of a token == 15min)  
                                        {"refresh": "<refresh_token>"}

___
### 4. Geo Address Endpoints
The final saved address in the db will be an IP.  
However, you can still use a URL or the hostname to perform such actions, 
because application will verify the IP address of a provided value.

    /add/        POST       Based on the passed address (ip/URL/hostname), create
                            Address, Language & AddressGeoData instances. 
                            
                            If the Address already exists in the db, create only the rest ones.

                                {"address": "ip/URL/hostname"}
                            
                            *Uses the external API to verify the final IP address of a provided
                            by user address (hostname, URL, IP, ...) & grab its geolocation data.
                       

    /delete/     DELETE     Based on the passed address (ip/URL/hostname), deletes 
                            an AddressGeoData instance (not an Address!).

                                {"address": "IP/url/hostname"}

                            *If the provided Address is not present in the db, uses the 
                            external API to verify the final IP address.


    /provide/    POST       It is a manual option for adding some geo data for an address.

                            Based on the passed data, creates the Language & AddressGeoData
                            instances for a existing in the db address.

                            *If the provided Address is not present in the db, uses the 
                            external API to verify the final IP address.


    /list/       GET        Lists Address instances with their one to one assigned 
                            AddresGeoData instances.
                            
___
### 5. Prerequisites for setting it locally
1. Docker
2. docker-compose
3. Linux os system

___
### 6. Setup
Run those commands in the top directory (where docker files are).

To build & set up the project:
>docker-compose up -d  

To migrate migrations:
>docker-compose exec web python manage.py migrate

To add initial data:
>docker-compose exec web python manage.py add_initial_data

To create a superuser (admin):
>docker-compose exec web python manage.py createsuperuser

To shut down the app:
>docker-compose down

___
### 7. Debugging
To check the logs:
>docker-compose logs

When somehow web service has raised before db:
>docker-compose restart web


___
### 8. Packages used
Described in the "requirements.txt"
1. Django==3.1.6
2. djangorestframework==3.12.2
3. djangorestframework-simplejwt==4.6.0
4. python-dotenv==0.15.0
5. requests=2.25.1
6. psycopg2==2.8.6
7. gunicorn==20.0.4
8. django-heroku==0.3.1

PostgreSQL as a db.  
JSON as a primary format.