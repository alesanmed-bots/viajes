# -*- coding: utf-8 -*-

import argparse
from bs4 import BeautifulSoup as bs
import urllib.request
from tools.parse_travel import parse_travel
from tools.user_agent import get_user_agent
import time
import logging
from mongodb import transactions

def run(logdir):
    URL = "http://www.exprimeviajes.com/"
    logger = logging.getLogger('viajes');
    logger.setLevel(logging.DEBUG);

    fileHandler = logging.FileHandler('{0}/viajesservice.log'.format(logdir));
    fileHandler.setLevel(logging.DEBUG);

    formatter = logging.Formatter(fmt='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    
    while True:
        req = urllib.request.Request(
                            URL,
                            data=None,
                            headers= {
                                'User-Agent': get_user_agent()
                                }
                            )
        document = urllib.request.urlopen(req)
        
        # Only for the development stage
        # with open('test.txt', 'r') as file:
        #    document = file.read()
        
        transactions.connect()
        web = bs(document, "html.parser")
        
        last_url = transactions.get_last_to_check()
        first = True
        
        for h2 in web.findAll('h2', class_="entry-title"):
            link = h2.a['href']
            if last_url is not None and link == last_url:
                transactions.disconnect()
                logger.debug("Last travel reached, going to sleep...")
                time.sleep(7200)
                break

                
            title = h2.a.text.strip().split()
            price = int(title[title.index("EUROS") - 1])
            try:
                transactions.save_travel(parse_travel(link, price))
            except Exception as e:
                logger.error(str(e))
            
            if first:
                first = False
                transactions.update_last_to_check(link)
            time.sleep(3)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("logdir", help="Defines where to store de log info. The user who runs the script must have write permissions in logging directory.")
    args = parser.parse_args()
    run(args.logdir)