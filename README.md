# Concert-ticket-scraping

Scraping all ticket information and seller contact which sold in secondary market within Thailand. Include Kaidee, TicketDee, PantipMarket and Facebook group

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites


```
Python 3.0 or above
Docker version 18.0 or above
```

## Installation

```
git clone https://github.com/snn2spade/concert-ticket-scraping.git
```

### Setup Scrapyd and Selenium Server using Docker Composer

Change directory to folder which containa docker-composer.yml

```
docker-composer up -d
```

After that we must see both Scrapyd and Selenium Server is started on Docker container

```
docker ps
```

### Deploy Scrapy crawler

Install scrapyd-client a client for Scrapyd which allows you to deploy your project to a Scrapyd server.

```
pip install scrapyd-client
```
Change directory to project root folder (folder which contain settings.py

```
scrapyd-deploy
```

Now go to http://localhost:6800 you must see Scrapyd server is running with ConcertScraper project

### Let try scraping concert ticket!

``` 
scrapy-client schedule kaidee -p ConcertScraper
```

This will scraping ticket sold on Kaidee with specifc keyword 'Celine' (You can change it later)
Now go to http://localhost:6800 and go to log section you will see job is running.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
