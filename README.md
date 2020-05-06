# Project 1

Web Programming with Python and JavaScript

Breif description: This is a book app made with flask and python. To use this website features you have to register first. Anyone can register in this website. After registration you will be able to log into the website and then you could people search for books, submit your reviews on different books and you could look at other different reviews from other people. User can't leave more than one review on the same book.

Features:
Login: When login page appears and user input his email and password - app will compare the informations with informations that are already saved in database. If the username and password match then user will be logged in and allowed to go to account page, if the user is already registered error message will show. Once the user is logged in, user will be able to look at his username on the navigation bar.

Registration: New user can register on the website. Before registration app will check if there is already any account registered with the same data. If the app does not find any matches it will register the account in the website.

Logout: Users can log out from the website by clicking on the logout button.

Search: By clicking the search menu button Users can search books by Title or Author or Year or ISBN number. If user submit the keyword in the search bar a search result table will appear with book list with that information.

Book page: By clicking a book title from the search result users can view information about that book. Statical information will come from goodread.com api and reviews data will come from my website database.

db URI: postgres://okbazksspizzvy:ed42cf8e50a9824eebc6e21d4d9ac34f0250eaeb75f6cc4d16ca9a41a31a7de1@ec2-54-217-204-34.eu-west-1.compute.amazonaws.com:5432/dacegb38d1f5r2

# Screenshots
# Home
![Screenshot](static/img/homee.jpg)
# Registration
![Screenshot](static/img/register.jpg)
# Login
![Screenshot](static/img/login.jpg)
# Search
![Screenshot](static/img/search.jpg)
