# :moneybag: auctions_

_auctions_ is a marketplace application built with Python and Django, where users make secret bids on each other's products and the winner takes home the goodies when the bidding is closed.

__tldr:__
- Django! Data models! Forms! Bootstrap! Authentication! Dynamic templating!
- favourite code snippet:
```Python
  if winner == None:
      messages.info(
        request, 
        f"Bidding for {closing.listing_auction.title} - sorry that nobody bid high enough this time."
      )
  else:
      messages.success(
        request, 
        f"Going... Going... Gone! Sold '{closing.listing_auction.title}' for £{winner.bid_amount:.2f}."
      )
```
- what it looks like:

![auction screenshot](https://s3.eu-west-2.amazonaws.com/media.jh-portfolio/media/project_images/auction-2.png)

Completed as part of Harvard's [CS50’s Web Programming with Python and JavaScript](https://online-learning.harvard.edu/course/cs50s-web-programming-python-and-javascript)
course, _auctions_ was the perfect chance for an exploration of Django's models, views, templates, forms and admin interface.

As well as providing a lot to play around with on the backend, the frontend of the application provided an opportunity to experiment with layouts. The application templates contained various conditionals according to permissions, open and closed listings, watched and bidded on items, so there was plenty to consider with how to present the dynamic content.

I've read a lot about object related programming, but this was the first time that I've worked with Django models. Interacting with models and objects definitely took a bit of getting used to at first, but after the inital mapping out of the models, I really enjoyed the freedom of not having to interact directly with SQL. The CS50 courses do an excellent job of gradually adding the layers of abstraction to your programming so that you can fully appreciate the worth of each tool that is introduced.
