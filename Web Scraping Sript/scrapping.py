from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import json
import os
import pickle
import hashlib
import psycopg2
import re

def deleteRestaurant(name, cnxn):

    cur = cnxn.cursor()
    cur.execute("CALL RestaurantDelete(%s);", (name,))
    cnxn.commit()
    cur.close()

    print(f"{name} deleted in database.")

def updateRestaurant(restaurant_info, cnxn):

    # Create a list of facility by boolean check
    facility_bools = []
    ALL_FACILITY = ['24 Hours', 'Birthday Party', 'Breakfast', 'Cashless Facility', 'Dessert Center', 'Drive-Thru', 'McCafe', 'McDelivery', 'Surau','WiFi', 'Digital Order Kiosk', 'Electric Vehicle']
    for x in ALL_FACILITY:
        if x in restaurant_info['facilities']:
            facility_bools.append(True)
        else:
            facility_bools.append(False)

    params = (restaurant_info['name'], restaurant_info['address'], restaurant_info['latitude'], restaurant_info['longitude'], restaurant_info['postcode'], "Kuala Lumpur", restaurant_info['waze_url'], *facility_bools)

    cur = cnxn.cursor()
    cur.execute("CALL RestaurantUpdate(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", params)
    cnxn.commit()
    cur.close()

    print(f"{restaurant_info['name']} updated in database.")

def insertRestaurant(restaurant_info, cnxn):

    # Create a list of facility by boolean check
    facility_bools = []
    ALL_FACILITY = ['24 Hours', 'Birthday Party', 'Breakfast', 'Cashless Facility', 'Dessert Center', 'Drive-Thru', 'McCafe', 'McDelivery', 'Surau','WiFi', 'Digital Order Kiosk', 'Electric Vehicle']
    for x in ALL_FACILITY:
        if x in restaurant_info['facilities']:
            facility_bools.append(True)
        else:
            facility_bools.append(False)

    params = (restaurant_info['name'], restaurant_info['address'], restaurant_info['latitude'], restaurant_info['longitude'], restaurant_info['postcode'], "Kuala Lumpur", restaurant_info['waze_url'], *facility_bools)

    cur = cnxn.cursor()
    cur.execute("CALL RestaurantInsert(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", params)
    cnxn.commit()
    cur.close()

    print(f"{restaurant_info['name']} inserted in database.")

def initDB_cnxn():
    cnxn = psycopg2.connect(
        dbname="",
        user="",
        password="",
        host="",
        port=""
    )

    return cnxn 

def run_selenium():
    # Set up Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.mcdonalds.com.my/locate-us")
    
    # Select "Kuala Lumpur" from dropdown
    select = Select(driver.find_element(By.ID, "states"))
    select.select_by_visible_text("Kuala Lumpur")
    
    # Wait for the page to update
    time.sleep(3)  # Adjust based on site loading time
    
    # Get updated HTML content
    html_content = driver.page_source
    
    ## DEBUGGING - Write to html 
    #with open("DEBUGGING_kl.html", "w", encoding="utf-8") as file:
    #    file.write(html_content)
    #print(" - Updated HTML content to raw_kl.html.")
    
    driver.quit()

    return html_content

def generate_hash(restaurant):
    key_str = f"{restaurant['name']}_{restaurant['address']}_{restaurant['facilities']}"
    return hashlib.md5(key_str.encode()).hexdigest()

def regex_postcode(address):
    postcode_pattern = re.compile(r"\b\d{5}\b")
    match = postcode_pattern.search(address)

    if match:
        return match.group()
    else:
        return "N/A"

def scrap_site():

    cnxn = initDB_cnxn()

    ## DEBUGGING - read from html
    #with open("DEBUGGING_raw.html", "r", encoding="utf-8") as file:
    #    html_content = file.read()
    #print(" - Read HTML content from raw_kl.html.")
    
    html_content = run_selenium()

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    restaurant_divs = soup.find_all("div", class_="addressBox")

    if os.path.exists("sync_hash.pkl"):
        with open("sync_hash.pkl", "rb") as file:
            existing_hashes = pickle.load(file)
    else:
        existing_hashes = {}  
    
    new_restaurants_list = [] 
    for restaurant_div in restaurant_divs:
        restaurant_info = {}

        # Extract from html element 
        name_tag = restaurant_div.find("a", class_="addressTitle")
        address_tag = restaurant_div.find("p", class_="addressText")
        # Extract facilities 
        facilities = [facility.text.strip() for facility in restaurant_div.find_all("span", class_="ed-tooltiptext")]
        # Extract latitude and longitude from script tag for waze url
        script_tag = restaurant_div.find("script", type="application/ld+json")
        data = json.loads(script_tag.string)
        latitude = data.get("geo", {}).get("latitude")
        longitude = data.get("geo", {}).get("longitude")
        waze_url = f"https://www.waze.com/en-GB/live-map/directions?navigate=yes&to=ll.{latitude}%2C{longitude}"
        # Regex from address to get postcode
        postcode = regex_postcode(address_tag.text.strip() if address_tag else "N/A")
        
        restaurant_info['name'] = name_tag.text.strip() if name_tag else "N/A"
        restaurant_info['address']= address_tag.text.strip() if address_tag else "N/A"
        restaurant_info['facilities']= facilities if facilities else "N/A"
        restaurant_info['latitude']= latitude if latitude else "N/A"
        restaurant_info['longitude']= longitude if longitude else "N/A"
        restaurant_info['postcode']= postcode if postcode else "N/A"
        restaurant_info['waze_url']= waze_url if waze_url else "N/A"

        new_restaurant_hash = generate_hash(restaurant_info)

        if restaurant_info['name'] in existing_hashes.keys():
            if new_restaurant_hash == existing_hashes[restaurant_info['name']]: # 1. No Update
                print(f"{new_restaurant_hash} ::::: {restaurant_info['name']} Synchronized.")
                new_restaurants_list.append(restaurant_info)
            else: # 2. Update on existing restaurant
                updateRestaurant(restaurant_info, cnxn)
                new_restaurants_list.append(restaurant_info) 
                existing_hashes[restaurant_info['name']] = new_restaurant_hash
        else: # 3. New Restaurant 
            insertRestaurant(restaurant_info, cnxn)
            new_restaurants_list.append(restaurant_info)
            existing_hashes[restaurant_info['name']] = new_restaurant_hash 

    existing_restaurant_names = set(existing_hashes.keys())
    new_restaurant_names = {restaurant['name'] for restaurant in new_restaurants_list}
    removed_restaurants = existing_restaurant_names - new_restaurant_names
    if removed_restaurants: # 4. Removed Restaurant
        for name in removed_restaurants:
            deleteRestaurant(name, cnxn)
            del existing_hashes[name]

    with open("sync_hash.pkl", "wb") as file:
        pickle.dump(existing_hashes, file)

    ## DEBUGGING - Write to txt
    #with open("DEBUGGING_restaurant_information.txt", "w", encoding="utf-8") as file:
    #    for restaurant_info in new_restaurants_list:
    #        for key, value in restaurant_info.items():
    #            file.write(f"{key}: {value}\n")
    #        file.write("\n")
    #print(" - Extracted information from html.")



if __name__ == "__main__":
    scrap_site()