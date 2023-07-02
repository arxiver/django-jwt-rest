# Welcome to LMS

## How to get started
3. Create a virtual environment ```virtualenv venv```
4. Activate the virtual environment ```source venv/bin/activate```
5. Install the requirements ```pip3 install -r requirements.txt```
6. Run the migrations ``` python manage.py makemigrations core```
6. Run the migrations ```python manage.py migrate```
8. Run the server ```python manage.py runserver```
9. Visit the server at ```http://localhost:8000``` which will show you the API documentation

## Stack
- Django
- Django Rest Framework
- SQLite
- Swagger

## Context

![context](./assets/context.jpeg)


## System Architecture
![architecture](./assets/architecture.jpeg)

## API Documentation
![api](./assets/api.png)

## Demo
- Signup (toggle between is_borrower and is_investor): [Signing up as a borrower](./demo/0-signup.webm)
- Investor & Borrower: [Login](./demo/0-login.webm)
- Borrower: [Create a loan request](./demo/1-create_loan_req.mp4)
- Borrower: [Get my loan requests](./demo/2-get_loan_requests.webm)
- Investor: [Create offer](./demo/3-create_offer.webm)
- Investor: [Get my offers](./demo/4-get_my_offers.webm)
- Borrower: [Check offers on my loan request](./demo/5-check_requests_offers.webm)
- Borrower: [Accept offer](./demo/6-accept_offer.webm)