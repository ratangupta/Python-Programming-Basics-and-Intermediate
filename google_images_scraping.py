# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:00:19 2020

@author: ratan
"""

from selenium import webdriver
import time
import requests
import os
import io
import hashlib
from PIL import Image


class image_downloader:
    
    def __init__(self, search_item, number_of_images, wd):
        self.search_item = search_item
        self.number_of_images = number_of_images
        self.wd = wd
      
    '''Function to fetch image urls
       It scrolls through the google images webpage, clicks on the thumbnails one by one 
       and retrieves images behind the thumbnails
       Arguments passed: search item, number of images the user wants, webdriver
       Returns: a set of image urls
    '''    
    def fetch_image_urls(self, keyword, max_images_to_fetch, wd, sleep_between_interactions = 1):
        
        # A function to scroll through a webpage
        def scroll_to_end(wd):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleep_between_interactions)    
        
        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={key}&oq={key}&gs_l=img"
    
        # Load the page
        wd.get(search_url.format(key=keyword))
    
        image_urls = set()
        image_count = 0
        start_results = 0
        
        while image_count < max_images_to_fetch:
            scroll_to_end(wd)
    
            # Getting all image thumbnails
            thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
            number_of_results = len(thumbnail_results)
            
            print("FOUND: {} search results. Extracting links from {}:{}".format(number_of_results, start_results, number_of_results))
            
            for img in thumbnail_results[start_results:number_of_results]:
                # Try to click every thumbnail on the webpage in order to get the real image behind it
                try:
                    img.click()
                    time.sleep(sleep_between_interactions)
                
                except Exception:
                    continue
    
                # Extract image urls by using css selector to specify one html tag
                actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
                for actual_image in actual_images:
                    if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                        image_urls.add(actual_image.get_attribute('src'))
    
                image_count = len(image_urls)
    
                if len(image_urls) >= max_images_to_fetch:
                    print("FOUND: {} image links".format(len(image_urls)))
                    break
            
            else:
                print("Found:", len(image_urls), "image links, looking for more ...")
                time.sleep(30)
                return 
                load_more_button = wd.find_element_by_css_selector(".mye4qd")
                    
                if load_more_button:
                    wd.execute_script("document.querySelector('.mye4qd').click();")
        
                # move the result startpoint further down
                start_results = len(thumbnail_results)

        return image_urls
    
    
    '''Function to save images in the directory created by download()
        It takes the following arguments: image url and path of the target folder
        It does not return anything'''
    def save_image(self, folder_path, url):
        
        try:
            image_content = requests.get(url).content
    
        except Exception as e:
            print("FAILURE! Could not download {} : {}".format(url, e))
    
        try:
            image_file = io.BytesIO(image_content) # Creating an in-memort buffer stream (using RAM)
            image = Image.open(image_file).convert('RGB') 
            file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality = 85) # Saving images with JPEG extension
            
            print("SUCCESS! Saved {} as {}".format(url, file_path))
        
        except Exception as e:
            print("FAILURE! Could not save {} : {}".format(url, e))
    
    
    ''' Function to make a directory(to store images) named the keyword user entered, 
        call functions to fetch image urls and save images
        It takes the following arguments: 
            keyword for images are needed, 
            number of images and 
            path to make directory
        It does not return anything'''
    def download(self, search_term, number_of_images, target_path='./images'):
        
        target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))
        
        if not os.path.exists(target_folder):
            os.makedirs(target_folder) # Create a directory
    
        # Calling a function to fetch all image urls    
        with self.wd as wd:
            image_urls = self.fetch_image_urls(search_term, number_of_images, wd, sleep_between_interactions = 0.5)
            
        # Calling a function to save all images    
        for element in image_urls:
            self.save_image(target_folder, element)


''' Function to get the webdriver specific to user's choice of browser
    It takes user's choice of browser as argument and returns the webdriver'''
def choose_browser(browser):
    if browser == 1:
        wd = webdriver.Chrome()
    elif browser == 2:
        wd = webdriver.Firefox()
    elif browser == 3:
        wd = webdriver.Safari()
    elif browser == 4:
        wd = webdriver.Opera()
    elif browser == 5:
        wd = webdriver.Edge()
        
    return wd


def main():
    search_term = input("Enter the keyword for which you want to dowload images off the internet: \n")
    number_of_images = int(input("Enter the number of images you want: \n"))
    browser = int(input("What browser do you want to use? 1. Chrome  2. Firefox  3. Safari  4. Opera  5. Edge: \n"))
    
    wd = choose_browser(browser) # Getting the webdriver specific to user's choice of browser
    
    image_obj = image_downloader(search_term, number_of_images, wd) # Initialising object of image_downloader class
    image_obj.download(search_term, number_of_images) # Searching for images the user wants and downloading them
    
    
if __name__ == '__main__':
    main()