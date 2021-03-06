# Concert-ticket-scraping

Scraping all ticket information and seller contact which sold in secondary market within Thailand. Include Kaidee, TicketDee, PantipMarket and Facebook group

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Note

Since PantipMarket is block IP Address outside Thailand, So if you deploy server on foriegn country it won't work only
PantipMarket.

### Prerequisites


```
Python 3.0 or above
Pip 2.0 or above
Docker version 18.0 or above
```

## Installation

```
git clone https://github.com/snn2spade/concert-ticket-scraping.git
```

### Setup Scrapyd and Selenium Server using Docker Composer

Change directory to folder which containa docker-composer.yml

```
docker-compose up -d
```

After that we must see both Scrapyd and Selenium Server is started on Docker container

```
docker ps
```

### Create Settings.py file

Go to root folder and copy template-settings.py to settings.py 

```
cp template-settings.py settings.py
```


### Deploy Scrapy crawler

Install scrapyd-client a client for Scrapyd which allows you to deploy your project to a Scrapyd server.

```
pip install git+https://github.com/scrapy/scrapyd-client
which scrapyd-client
```
Change directory to project root folder (folder which contain settings.py)

```
scrapyd-deploy
```

Now go to http://localhost:6800 you must see Scrapyd server is running with ConcertScraper project

### Let try scraping concert ticket!

``` 
scrapy-client schedule kaidee -p ConcertScraper
```

This will scraping ticket sold on Kaidee with specifc keyword 'Celine' (You can change it in settings.py)

Now go to http://localhost:6800 and go to log section you will see job is running.

## Schedule Async check on Ubuntu

First, create bash script

```
#!/bin/bash
PATH=/opt/someApp/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
scrapyd-client schedule -p ConcertScraper kaidee
scrapyd-client schedule -p ConcertScraper ticketdee
#scrapyd-client schedule -p ConcertScraper pantipmarket
scrapyd-client schedule -p ConcertScraper facebook
```

Then enable to execute this file

```
chmod 777 {path-to-script}
```

Next, edit crontab configuration

```
crontab -e
```

then add this line below

```
*/30 * * * * {path to script}
```

This will schedule every 30 miniute.

## Future

In nearest future I wil update not only for Concert ticket but everything! in e-commerce platform
But actually it not hard to modify, Let do this by yourself!


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
