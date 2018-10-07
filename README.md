# backpack-amazon-1M-search-engine

part 2 of the recruitment project

## Getting Started

*  Used the 10k asins from part1 to get their similar asins (for generating bulk asins)
*  Scraped {"title", "image", "price"} for each product. 
*  uploaded the json data to elasticsearch.
*  Searched by text, prefix, compared by price from their index and return corresponding record.


### Questions

* How long is takes to get all the data for 1M products? Can you make it faster? How?
  * For my case, I could scrape 130+ data in one hour.
  * To make it faster :
    * I need to test my code and debug, handle multithreading more accurately. 
    * Use Cloud Storage Services i.e AWS Cloud storage. As per given requirements, atmost $50 I can get more than 2.3TB storage in Amazon S3 ($0.021 per GB). It lets you store data at any format, provides many query services for big data handling & flexible data transfer at any geolocation.
    * Use Amazon Cloudsearch for auto scaling for data and traffic & self-healing. For search.m3.2xlarge (16-32GB), the costing is $0.752 per Hour, which fits the following constraints.
    * The budget can be increased.
    
* For each field, what % of the items are missing that field? Any idea why and how to minimize?
  * For the "title" and "image" fields, atmost 30% of the items were missed. But for the "price" field, more than 50% ietms were missed and I couldn't find out the solution. 
  * My code needs be more flexible to scrape data in all types of markups and layouts with handling the exceptions too.
 
* Approximately, how much will it cost every time you’ll refresh your inventory? How to bring that down?
  * With Amazon Coudsearch, atmost $19 is needed for 850GB to per hour.
  * Deploying more server can be solution. Clustering the data in multiple aws regions can be a solution.

* How to scale this to 10M items? Or 100M?
  * Implementing proper instances according to need in aws (cpu optimized/memory optimized)
  * Implementing the storage in different availablity zones with master-slave replication.
  * Implementing load balancer and elasticache in a proper manner to handle huge requests.
  * Make the scraper bug free by handing all kind of layouts/markups and exception handling.
  * Implementing parallelism at its level best.


