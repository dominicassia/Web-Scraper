# Web Scraper
A simple-tasked web scraper hosted on Heroku <br>
*Created December 2020* <br>
`Python` `Heroku` `Discord` `Requests` `Json`

## Table of Contents
1. Overview
2. Environment
3. Design
4. Results

## Overview
1. Gets Chrome webdriver with Selenium
2. Uses webdriver to open url
3. Fetched title with webdriver attribute
4. Writes title with timestamp to json file
5. Sends webhook via Requests POST to discord channel

This Heroku app utilizes the Python Requests library to retrieve the contents of a specified url. The received response will be parsed using 

This simple heroku app will serve the functionality of scraping the title of nike's website, saving it in a json file, and sending it to a discord server via webhook. The process includes scraping the page source with selenium, using beautiful soup to parse the html, and thus extracting the title.

This practice repository is the elementary concept behind [Pat-Potbot](https://github.com/dominicassia/pat-potbot)

The discord bot will be async
