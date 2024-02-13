#  --- chatgpt code 

import requests
from bs4 import BeautifulSoup
import csv
import os
import time
from selenium import webdriver
from urllib.parse import urljoin

# Define the URL of the website
url = "https://www.politifact.com/"

# Send a GET request to fetch the webpage content
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Function to extract text content recursively
def extract_text(soup):
    text_content = []

    # Find all text elements
    for element in soup.find_all(text=True):
        # Exclude script and style elements
        if element.parent.name not in ["script", "style"]:
            text = element.strip()
            if text:
                text_content.append(text)

    return text_content

# Function to extract images and download them
def extract_images(soup, folder_path):
    image_links = []

    # Find all image elements
    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            image_links.append(src)
            # Download the image
            image_url = urljoin(url, src)
            image_name = src.split("/")[-1]
            image_path = os.path.join(folder_path, image_name)
            with open(image_path, "wb") as f:
                f.write(requests.get(image_url).content)

    return image_links

# Function to extract videos and download them
def extract_videos(soup, folder_path):
    video_links = []

    # Find all video elements
    for video in soup.find_all("video"):
        src = video.get("src")
        if src:
            video_links.append(src)
            # Download the video
            video_url = urljoin(url, src)
            video_name = src.split("/")[-1]
            video_path = os.path.join(folder_path, video_name)
            with open(video_path, "wb") as f:
                f.write(requests.get(video_url).content)

    return video_links

# Function to scroll down the page to load more content
def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Set up a headless Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run headless browser
driver = webdriver.Chrome(options=options)
driver.get(url)

# Scroll down to load more content
scroll_page(driver)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Extract text content
text_content = extract_text(soup)

# Create a folder named "data" if it doesn't exist
folder_path = "alt"
os.makedirs(folder_path, exist_ok=True)

# Extract image links and download images
image_links = extract_images(soup, folder_path)

# Extract video links and download videos
video_links = extract_videos(soup, folder_path)

# Define the path for the CSV files within the "data" folder
text_csv_file = os.path.join(folder_path, "mastodon_text.csv")
image_csv_file = os.path.join(folder_path, "mastodon_images.csv")
video_csv_file = os.path.join(folder_path, "mastodon_videos.csv")

# Write the text content to a CSV file
with open(text_csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter="\t")

    # Write the header row
    writer.writerow(["Text"])

    # Write each text content to a separate row
    for text in text_content:
        writer.writerow([text])

# Write the image links to a CSV file
with open(image_csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter="\t")

    # Write the header row
    writer.writerow(["Image Link"])

    # Write each image link to a separate row
    for link in image_links:
        writer.writerow([link])

# Write the video links to a CSV file
with open(video_csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter="\t")

    # Write the header row
    writer.writerow(["Video Link"])

    # Write each video link to a separate row
    for link in video_links:
        writer.writerow([link])

print("Text content has been saved to", text_csv_file)
print("Image links have been saved to", image_csv_file)
print("Video links have been saved to", video_csv_file)

# Quit the WebDriver session
driver.quit()
