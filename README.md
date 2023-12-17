# Commerce
This is a e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

# Installation 

To use this project first you need python and django

To install django
```bash
pip3 install Django
```

To run the project
```bash
python3 manage.py runserver
```

If you change anything in ``àuctions/models.py``, you'll need to first run this commands to migrate those changes to your database
```bash
python3 manage.py makemigrations
```

```bash
python manage.py migrate
```

To create a superuser account that can access Django's admin interface
```bash
python3 manage.py createsuperuser
```

# Demo

Here it is a simple usage example on YouTube: [TODO](https://youtu.be/U5ZnqcuSNv4).

## Models

The application have five models: ``AuctionListings``, ``Bids``, ``Comments``, ``Category`` and ``User``.

## Create Listing

Users will be able to visit a page to create a new listing. They can specify a title for the listing, a text-based description, and what the starting bid should be. Users also optionally will be able to provide a URL for an image for the listing and a ``Category``.

## Active Listing Page

It's the default route of this web application and users can view all of the currently active auction listing. For each active listing, the page display the title, description, current price and photo.

## Listing Page

Clicking on a listing will take users to a page specific to that listing. On that page, users will be able to view all details about the listing, including the current price for the listing. If the user is signed he will have the following options:
  * Add the item to their ``Watchlist``, if the item is already on the watchlist, the user will be able to remove it.
  * Bid on the item, the bid must be at least as large as the starting bid, and must be greater tahn anyu other bids that have been placed. If not the user will be presented with an error.
  * Add comments to the listing page. The listing page will display all comments that have been made on the listing.
  * If he is signed and is the one who created the listing, he will be able to "close" the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active. The page will inform the user who has won when he enters the page.

## Watchlist

Users who are signed in can visit a Watchlist page, which will display all of the listings that a user had added to their watchlist. Clicking on any of those listings should take the user to that listing's page.

## Categories
Users can visit a page that displays a list of all listing categories. Clicking on the name of any category will take the user to a page that displays all of the active listing in that category.

## Django Admin Interface

Via the Django admin interface, a site administrator will be able to view, add, edit and delete any listings, comments and bids made on the site

