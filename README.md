# Hotels

***Live Demo:*** [https://hotels.reuelrds.me](https://hotels.reuelrds.me/)

A simple website for displaying Hotel Recommendations.  
The Front End is built using the Angular Framework, while the Backend has a REST API built using the Flask Framework and uses SQLite database to store data.

Currently only supports Desktop Resolution (1920x1080)

&nbsp;  

Table of Contents:
- [Final-Project](#final-project)
  - [Scrapper](#scrapper)
  - [Frontend](#frontend)
  - [Backend](#backend)
  - [Project Setup](#project-setup)
    - [Clone this Repo](#clone-this-repo)
  - [Run the Project](#run-the-project)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## Scrapper

The project also used Scrapy to scrape data of 481 Hotels off the Tripadvisor Website. We used Selenium to render the hotel webpage before using scrapy to scrape the details off the website.

We scrapped the following fields from the tripadvisor website:

* _Hotel Name_
* _Hotel Address_
* _Review Count_
* _Rating_
* _Hotel Description_
* _Hotel Price for a single night of reservation_


The last four fields were filled with randomly generated data as some of the hotel webpages did not have that information.


We used Rotating Proxies from [ScraperApi](https://www.scraperapi.com/) to get around Tripadvisor's scrapping limits.


After, scrpaing we post processed the data to add the Hotel's Reviews, City, and Country from the Dataset used for Machine Learning.



## Frontend

The Website is split into multiple components because we are using Angular Framework. We have used SASS as a preprocessor for the stylesheets (CSS) and Typescript inplace of JavaScript.

All the web components are grouped under the `views` folder. Each of these web components consists of a HTML file, a SASS Style Sheet, and a TypeScript File which are linked together to make up the web component.

These web components are linked to the backend through Services which communicate with the backend to fetch and handle data. These services are just regular Typescript files, grouped under the `services` folder, which send HTTP Requests to the Backend and are handle the fetched data. They are also used to store data and pass the data to the web component when the web component requests the data.

We use `rxjs` library to pass this data around the websit and allows us to handle asynchronous data more efficiently.

The Frontend has the following routes:
|                       |                           |
|-----------------------|---------------------------|
| _/_                   | Home Page                 |
| _/auth/signup_        | Reigsteration Page        |
| _/auth/login_         | Login Page                |
| _/recommend_           | Displays Hotel List       |
| */hotel/:hotel_id*    | Displays Hotel Details    |

&nbsp;

The `core` folder has a typescript file which protects (does not allow users to browse) the `_/recommend` and the `/hotel/:hotel_id` routes unless the user is logged in.


Also, all the image assets are taken from [Unsplash](https://unsplash.com/).




## Backend

We used Flask to create an REST API because it would allow us to easily call the Recommendation function from the Machine Learning part of the project. This is a simple api with the following endpoints:

|                           |                                   |
|---------------------------|-----------------------------------|
| _/auth/signup_            | Reigster an User                  |
| _/auth/login_             | Log in an User                    |
| _/destinations_           | Get a List of Hotel Destinations  |
| _/hotels_                 | Get Hotel                         |
| */reviews/:hotel_id*      | Get Hotel Reviews                 |


The first two endpoints only support POST request and the other three just support GET requests. The response data is sent to the Frontend in JSON format.

We use JSON Web Tokens (JWT) instead Session tokens or Cookies to maintaining sessions and user authorization. This token is generated and sent to the user when they register or log in.

The `/hotels` and the `/reviews/:hotel_id` endpoints are protected and cannot be accessed unless the JWT token is valid. The requests to these endpoints require a valid JWT token present in the Request's `Authentication` Header.


The Frontend has an TypeScript File in the `core` folder which intercepts all the requests from the `Services` to the backend. It adds this `Authentication` header to the request, if the user is logged in, before sending it to the backend.


## Project Setup

***TODO:  Update steps about how to setup the project***

### Clone this Repo

```bash
> git clone https://github.com/reuelrds/Hotels.git
> cd Hotels
```

## Run the Project

***TODO:  Add in steps about how to tun the project***
