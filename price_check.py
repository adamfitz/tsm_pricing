#!/usr/bin/env python3


import requests
import json
import sys
from datetime import datetime, timezone

def main():
    api_key = load_api_key()
    returned_price_us = us_avg_price(api_key)
    returned_price_barthalis = avg_price_barthilas(api_key)

    

def load_api_key():
    # load api key out of a file so we dont have to store it in the script
    # there should be ONLY ONE api key in this file
    try:
        with open("api_key.txt", "r") as api_key_file:
            # read each line into the list
            api_key = api_key_file.readlines()
            # strip off the newline char from each element in the list
            api_key = [x.strip("\n") for x in api_key]
            # strip any whitespace
            api_key = [x.strip() for x in api_key]
            # convert the first list element to a string (the api key in the file)
            api_key = str(api_key[0])
        return api_key
    except FileNotFoundError as file_not_found:
        return "\n== api_key.txt file NOT found, Please check the file exists and contains your trade skill master api key. == \n"
        sys.exit(1)


def us_avg_price(api_key):

    #get current time
    #current_time_oceania = datetime.now(timezone.sydney)
    #current_time_utc = datetime.now(timezone.utc)

    # read in the items from text file
    item_dict = {}
    try:       
        with open("item_list.txt", "r") as item_list:
            for line in item_list:
                (key, value) = line.split(":")
                # strip off the carriage return and any whitespace
                line = line.strip("\n")
                line = line.strip()
                # populate dict with item name and item id
                item_dict[key] = value
        for key, value in item_dict.items():
            item_dict[key] = value.strip("\n")
    except Exception as read_item_list_failed:
        return "Reading items from file did not work...please check, the full error is shown below\n\n{}".format(read_item_list_failed)
    
    items_to_price_check = item_dict

    try:
        #print("US Average pricing data current as at: \nOceania: {}\nUTC: {}".format(current_time_oceania, current_time_utc))
        for name, item_id in items_to_price_check.items():
            if not item_id:
                print("Item id was not found, please check your item text file.")
                continue
            else:
                url = "http://api.tradeskillmaster.com/v1/item/{}?format=json&apiKey={}".format(item_id, api_key)
                

                # query tsm website for the item data
                response = requests.get(url)
                # get the json output
                json_data = json.loads(response.text)
                if "error" in json_data:
                    print("\nError in TSM API query, the full exception is shown below: \n{}\n".format(json_data))
                    sys.exit(1)
                else:
                    # define the average and min price
                    average_price_us = str(json_data["USMarketAvg"])
                    min_buyout_us = str(json_data["USMinBuyoutAvg"])
                    # slice the string to represent copper, silver and gold
                    average_price_us_copper = average_price_us[-2:]
                    average_price_us_silver = average_price_us[-4:-2]
                    average_price_us_gold = average_price_us[:-4]

                    us_average_total = average_price_us_gold + "g" + " " + average_price_us_silver + "s" + " " + average_price_us_copper + "c"
                    print("Item: {}\t\tAVG US Price: {}".format(name, us_average_total))
    
    except Exception as general_exception:
        print("General exception caught.  Please see below for the full error\n\n{}.".format(general_exception))

def avg_price_barthilas(api_key):

    region = "US"
    realm = "Barthilas"

    # read in the items from text file
    item_dict = {}
    try:       
        with open("item_list.txt", "r") as item_list:
            for line in item_list:
                (key, value) = line.split(":")
                # strip off the carriage return and any whitespace
                line = line.strip("\n")
                line = line.strip()
                # populate dict with item name and item id
                item_dict[key] = value
        for key, value in item_dict.items():
            item_dict[key] = value.strip("\n")
    except Exception as read_item_list_failed:
        return "Reading items from file did not work...please check, the full error is shown below\n\n{}".format(read_item_list_failed)

    items_to_price_check = item_dict

    try:
        #print("US Average pricing data current as at: \nOceania: {}\nUTC: {}".format(current_time_oceania, current_time_utc))
        for name, item_id in items_to_price_check.items():
            if not item_id:
                print("Item id was not found, please check your item text file.")
                continue
            else:
                url = "http://api.tradeskillmaster.com/v1/item/{}/{}/{}?format=json&apiKey={}".format(region, realm, item_id, api_key)   
                
                #query tsm website for the item data
                response = requests.get(url)
                # get the json output
                json_data = json.loads(response.text)
                if "error" in json_data:
                    print("\nError in TSM API query, the full exception is shown below: \n{}\n".format(json_data))
                    sys.exit(1)
                else:
                    # amount of current auctions and quantity
                    quantity = str(json_data["Quantity"])
                    number_of_auctions = str(json_data["NumAuctions"])
                    minimum_buyout_price = str(json_data["MinBuyout"])

                    min_buyout_copper = minimum_buyout_price[-2:]
                    min_buyout_silver = minimum_buyout_price[-4:-2]
                    min_buyout_gold = minimum_buyout_price[:-4]

                    barthilas_min_buyout_price = min_buyout_gold + "g" + " " + min_buyout_silver + "s" + " " + min_buyout_copper + "c"

                    print("Realm US Barthilas - Item: {}\tMin Buyout: {}\tNum of Auctions: {}\tQuantity: {}".format(name, barthilas_min_buyout_price, number_of_auctions, quantity))
    
    except Exception as general_exception:
        print("General exception caught.  Please see below for the full error\n\n{}.".format(general_exception))


if __name__ == "__main__":
    main()