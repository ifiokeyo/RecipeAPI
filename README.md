# PizzaAPI

 > A pizza api built with Django

## Requirements
 - Docker

## Development setup

 > Clone this repo and navigate into the project's directory


> Add a .env file in the root of the cloned project folder using the 
> sample_env file.


#### Start up the server

```bash
$ docker-compose up --build
```


#### Create a superuser (Admin user)

```bash
$ docker-compose run --rm app sh -c "python manage.py createsuperuser"
```


#### Run tests

 > Run tests using the commands below:

```bash
$ docker-compose run --rm app sh -c "python manage.py test && flake8"
```

 >  The app should now be available from your browser at http://127.0.0.1:2000

 > Test API with Postman.

##### Endpoints

 > For endpoints that require authentication, add a valid access token to the Request *Authorization header* - *Token <ACCESS TOKEN>*


- **Signup a user**

   POST */api/v1/user/create/*

    > Request Payload
     
    ```
    {
        "name": <full name>,
        "email": <email>,
        "password": <password min_length 8>  
    }
    ```

-  **Login a user**

   POST */api/v1/user/token/*

    > Request Payload 
    
    ```
    {
        "email": <email>,
        "password": <password min_length 8>  
    }
    ```

    
- **View User profile** `[JWT token required]`

    GET */api/v1/user/me/*
    
    
- **Update User detail** `[JWT token required]`

    PATCH */api/v1/user/me/*
    
    > Request Payload one or all of the fields below.
    
    ```
    {
	    "name": <new name>,
	    "password": <new password>
    }
    ```
    
- **Create pizza** `[JWT token required]`

    POST */api/v1/pizza/pizzas*
    
    > Request Payload
    
    ```
    {
	    "flavour": <name of pizza>,
	    "prices": {"S": <amount>, "M": <amount>, "L": <amount>}
    }
    ```
    
- **Get all pizzas** `[JWT token required]`

    GET */api/v1/pizza/pizzas*

    
- **Get a pizza detail** `[JWT token required]`

    GET */api/v1/pizza/pizzas/<pizza uuid>*
    
    
- **Update a pizza detail** `[JWT token required]`

    PATCH */api/v1/pizza/pizzas/<pizza uuid>*
    
    > Request Payload should contain one or all of the fields below.
    
    ```
    {
	    "flavour": <new name of pizza>,
	    "prices": {"S": <amount>, "M": <amount>, "L": <amount>}
    }
    ```
    
- **Delete a pizza** `[JWT token required]`

    DELETE */api/v1/pizza/pizzas/<pizza uuid>*
  
  
- **Retrieve all Orders** `[JWT token required]` `[Admin Required]`
    
    > Filtering using `status` query string takes in either or all of 
    > these values *'P'*, *'I'*, *'DN'*, *'DL'*
    
    
    GET */api/v1/order/admin/?status=*
    
    
- **Retrieve all orders for the logged-in user** `[JWT token required]`

    GET */api/v1/order/orders*
    

- **Create an order for the logged-in user** `[JWT token required]`

    GET */api/v1/order/orders*
    
    > Request payload 
    
    ```
    {
        "pizza_flavour": <flavour name>,
        "size": <"M" or "S" or "L">,
        "quantity": <Positive integer greater than 0>
    }
    ```
    
- **Update an order that has not been delivered for the logged-in user** `[JWT token required]`

    PATCH */api/v1/order/orders/<order uuid>*
    
    > Request payload should contain one or all of the fields below.
    > For the status field use the keys of this dictionary mapping below:
    
    ```python 
    {
        "P": "Pending",
        "I": "In-Progress",
        "DN": 'Done',
        "C": "Cancelled",
        "Delivered": 'Delivered'
    }
    ```
    
    ```
    {
        "pizza_flavour": <flavour name>,
        "size": <"M" or "S" or "L">,
        "quantity": <Positive integer greater than 0>
        "status"
    }
    ```
    
- **Delete an order for the logged-in user** `[JWT token required]`

    DELETE */api/v1/order/orders/<order uuid>*

