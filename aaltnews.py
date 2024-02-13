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
            'text': text
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


# Function to save data to files
def save_data(data, directory):
    if data is None:
        return  # If data is None, do not proceed with saving
    
    os.makedirs(directory, exist_ok=True)
    
    # CSV files for images and videos links
    images_csv_file = os.path.join(directory, 'image_links.csv')
    videos_csv_file = os.path.join(directory, 'video_links.csv')

    with open(images_csv_file, 'w', newline='', encoding='utf-8') as img_csv_file:
        img_csv_writer = csv.writer(img_csv_file)
        img_csv_writer.writerow(['Image Link'])
        for img in data['images']:
            img_url = img.get('src')
            if img_url:
                img_csv_writer.writerow([img_url])
                
    with open(videos_csv_file, 'w', newline='', encoding='utf-8') as vid_csv_file:
        vid_csv_writer = csv.writer(vid_csv_file)
        vid_csv_writer.writerow(['Video Link'])
        for vid in data['videos']:
            vid_url = vid.get('src')
            if vid_url:
                vid_csv_writer.writerow([vid_url])

    # Save text content to a text file
    with open(os.path.join(directory, 'text_content.txt'), 'w', encoding='utf-8') as txt_file:
        txt_file.write(data['text'])
        
    # Save images and videos to separate folders
    for key, value in data.items():
        if key in ['images', 'videos']:
            sub_directory = os.path.join(directory, key)
            os.makedirs(sub_directory, exist_ok=True)
            for i, media in enumerate(value):
                media_url = media.get('src')
                if media_url:
                    media_data = requests.get(media_url).content
                    with open(os.path.join(sub_directory, f'{key}_{i}.mp4' if key == 'videos' else f'{key}_{i}.png'), 'wb') as media_file:
                        media_file.write(media_data)

# Main function
def main():
    url = 'https://www.altnews.in/'  # Replace with your desired URL
    data = scrape_data(url)
    save_data(data, 'altnews')

if __name__ == "__main__":
    main()
