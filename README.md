Salford Bin Collection Notifications
------------------------------------

Small script that retrieves the next lot of bin collections from the Salford website and sends them to you via [Pushover](https://pushover.net).

You should edit the script and set the variables at the very top, then cron it to run every day at whatever time you want to recieve your notifications. It should run every day, rather than the day before your collection only, so that it picks up extra or changed collections immediately. By default it will notify you about collections happening the day after it runs, so you can put your bins out the night before.

Variables
---------

You need to set the following variables before running the script:

`UPRN`: You can get this by typing your postcode in [here](http://www.salford.gov.uk/bins-and-recycling/bin-collection-days/). The UPRN will be present at the end of the resulting URL after you've picked your address out of the list. e.g. `http://www.salford.gov.uk/bins-and-recycling/bin-collection-days/your-bin-collections/?UPRN=111111111111`.

`PUSHOVER_TOKEN`: Your Pushover app token.

`WHO`: A Python list containing the user tokens for the users you wish to notify about the upcoming collection.
