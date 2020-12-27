'''
    ### Simple-Heroku-App
    This simple heroku app will serve the functionality of
    scraping the title of nike's website, saving it in a json file,
    and sending it to a discord server via webhook. The scraping
    process will include scraping the page source with selenium,
    using beautiful soup to parse the html; extracting the title.  
'''

# -- Imports

import time

# ----

def main():
    pass

# ----

if __name__ == "__main__":
    # Repeat this process every day
    while True:
        main()
        time.sleep(86400)
