#  --- chatgpt code

import requests
from bs4 import BeautifulSoup
import os
import csv

def scrape_data(url):
    try:
        # Check if URL has a scheme
        if not url.startswith('http://') and not url.startswith('https://'):
            # Add the 'https://' scheme to the URL
            url = 'https://' + url
        
        # Make a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad response status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract images
        images = soup.find_all('img')
        # Extract videos
        videos = soup.find_all('video')
        # Extract audio
        audio = soup.find_all('audio')
        # Extract text
        text = soup.get_text()
        
        return {
            'images': images,
            'videos': videos,
            'audio': audio,
            'text': text,
            'image_links': [img.get('src') for img in images],
            'video_links': [vid.get('src') for vid in videos],
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

# Function to save data to files
def save_data(data, directory):
    if data is None:
        return  # If data is None, do not proceed with saving
    
    os.makedirs(directory, exist_ok=True)
    for key, value in data.items():
        if key == 'text':
            file_path = os.path.join(directory, f'{key}.txt')
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(value))
        elif key in ['images', 'videos', 'audio']:
            sub_directory = os.path.join(directory, key)
            os.makedirs(sub_directory, exist_ok=True)
            for i, media in enumerate(value):
                media_url = media.get('src')
                if media_url:
                    try:
                        media_data = requests.get(media_url).content
                        with open(os.path.join(sub_directory, f'{key}_{i}.png' if key == 'images' else f'{key}_{i}.mp4'), 'wb') as media_file:
                            media_file.write(media_data)
                    except requests.exceptions.RequestException as e:
                        print(f"Error fetching {key} {media_url}: {e}")
        elif key in ['image_links', 'video_links']:
            csv_file = os.path.join(directory, f'{key}.csv')
            with open(csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([f'{key.capitalize()}'])
                for link in value:
                    writer.writerow([link])

# Main function
def main():
    url = 'https://www.politifact.com/'  # Replace with your desired URL
    data = scrape_data(url)
    if data:
        save_data(data, 'politifact')

if __name__ == "__main__":
    main()
