#!/usr/bin/env python3
"""
YouTube Notes Generator
This script extracts information from YouTube videos and appends it to AINotesDump.md
"""

import os
import re
import sys
import time
import datetime
import traceback
import logging
import random
from urllib.parse import urlparse, parse_qs
import requests
import json

# Set up logging to file
logging.basicConfig(
    filename='youtube_notes.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'  # Overwrite log file each time
)

# Log both to file and console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

def log_exception(e):
    """Log exception with traceback to file"""
    logging.error(f"Exception: {str(e)}")
    logging.error(traceback.format_exc())

# Try different user agents to avoid blocking
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6324.211 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6324.211 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6324.211 Safari/537.36'
]

try:
    logging.info("Starting script execution")
    # First make sure we have the latest pytube
    try:
        import subprocess
        logging.info("Updating pytube to latest version")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pytube"])
        logging.info("Successfully updated pytube")
    except Exception as e:
        logging.warning(f"Could not update pytube: {e}")
        log_exception(e)
    
    from pytube import YouTube
    logging.info("Successfully imported pytube")
except ImportError:
    logging.error("Failed to import pytube, attempting to install")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytube"])
        from pytube import YouTube
        logging.info("Successfully installed and imported pytube")
    except Exception as e:
        logging.error("Failed to install pytube")
        log_exception(e)
        sys.exit(1)

def extract_video_id(url):
    """Extract the video ID from a YouTube URL"""
    logging.info(f"Extracting video ID from URL: {url}")
    # Handle different URL formats
    if 'youtu.be' in url:
        video_id = url.split('/')[-1].split('?')[0]
        logging.info(f"Extracted video ID (youtu.be format): {video_id}")
        return video_id
    
    parsed_url = urlparse(url)
    if 'youtube.com' in parsed_url.netloc:
        if '/watch' in parsed_url.path:
            video_id = parse_qs(parsed_url.query)['v'][0]
            logging.info(f"Extracted video ID (youtube.com/watch format): {video_id}")
            return video_id
        elif '/embed/' in parsed_url.path:
            video_id = parsed_url.path.split('/')[-1]
            logging.info(f"Extracted video ID (youtube.com/embed format): {video_id}")
            return video_id
        elif '/v/' in parsed_url.path:
            video_id = parsed_url.path.split('/')[-1]
            logging.info(f"Extracted video ID (youtube.com/v format): {video_id}")
            return video_id
    
    # If no video ID found, return the original URL (might be just the ID)
    logging.warning(f"Could not extract video ID, using URL as is: {url}")
    return url

def fallback_video_info(video_id):
    """Try to get video information using requests and parsing the page directly"""
    logging.info(f"Attempting fallback method to get video info for {video_id}")
    
    try:
        # Choose a random user agent
        user_agent = random.choice(USER_AGENTS)
        headers = {'User-Agent': user_agent}
        
        # Try to fetch the video page
        url = f"https://www.youtube.com/watch?v={video_id}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            logging.error(f"Fallback method failed with status code {response.status_code}")
            return None
        
        # Try to extract title from HTML
        html = response.text
        title_match = re.search(r'<title>(.*?) - YouTube</title>', html)
        title = title_match.group(1) if title_match else f"YouTube Video {video_id}"
        
        # Extract basic info
        info = {
            'title': title,
            'channel_name': 'Unknown (Fallback Method)',
            'thumbnail_url': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            'description': 'Description unavailable due to API restrictions',
            'publish_date': 'Unknown',
            'views': 'Unknown',
            'video_id': video_id,
            'duration': 'Unknown',
            'capture_date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'hashtags': 'None',
            'channel_subscribers': 'Unknown',
            'likes': 'Unknown',
            'comments': 'Unknown',
            'category': 'Unknown'
        }
        
        logging.info(f"Successfully retrieved basic info using fallback method: {title}")
        return info
    except Exception as e:
        logging.error(f"Error in fallback method: {e}")
        log_exception(e)
        return None

def get_video_info(url, max_retries=3):
    """Get information about a YouTube video"""
    try:
        video_id = extract_video_id(url)
        logging.info(f"Getting information for video ID: {video_id}")
        
        # Try with pytube multiple times with different user agents
        for attempt in range(max_retries):
            try:
                # Set a different user agent for each attempt
                user_agent = random.choice(USER_AGENTS)
                logging.info(f"Attempt {attempt+1}/{max_retries} with User-Agent: {user_agent}")
                
                # Create YouTube object with the selected user agent
                logging.info(f"Creating YouTube object for video ID: {video_id}")
                yt = YouTube(
                    f"https://www.youtube.com/watch?v={video_id}",
                    use_oauth=False,
                    allow_oauth_cache=False,
                    on_progress_callback=None
                )
                # Set user agent
                yt.headers = {'User-Agent': user_agent}
                
                logging.info(f"Successfully created YouTube object")
                
                # Basic video information
                logging.info("Extracting basic video information")
                info = {
                    'title': yt.title,
                    'channel_name': yt.author,
                    'thumbnail_url': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
                    'description': yt.description[:500] + "..." if len(yt.description) > 500 else yt.description,  # Truncate long descriptions in log
                    'publish_date': yt.publish_date.strftime('%Y-%m-%d') if yt.publish_date else 'Unknown',
                    'views': f"{yt.views:,}",
                    'video_id': video_id,
                    'duration': str(datetime.timedelta(seconds=yt.length)),
                    'capture_date': datetime.datetime.now().strftime('%Y-%m-%d'),
                }
                logging.info(f"Successfully extracted basic information: Title={info['title']}, Channel={info['channel_name']}")
                
                # Try to get additional information that may not always be available
                try:
                    logging.info("Extracting additional information")
                    # Get subscriber count - this requires additional API access
                    info['channel_subscribers'] = 'Unknown'  # Requires YouTube API with keys
                    
                    # Extract hashtags from description
                    hashtags = re.findall(r'#\w+', yt.description)
                    info['hashtags'] = ' '.join(hashtags) if hashtags else 'None'
                    logging.info(f"Found {len(hashtags)} hashtags")
                    
                    # This requires YouTube API with keys for accurate data
                    info['likes'] = 'Unknown'  # Requires YouTube API
                    info['comments'] = 'Unknown'  # Requires YouTube API
                    info['category'] = 'Unknown'  # Requires YouTube API
                    logging.info("Successfully extracted additional information")
                except Exception as e:
                    logging.warning(f"Could not get all extended information: {e}")
                    log_exception(e)
                
                return info
                
            except Exception as e:
                logging.warning(f"Attempt {attempt+1} failed: {e}")
                log_exception(e)
                
                # Wait before trying again, with increasing delay
                if attempt < max_retries - 1:
                    delay = (attempt + 1) * 2
                    logging.info(f"Waiting {delay} seconds before retrying...")
                    time.sleep(delay)
        
        # If pytube fails after all retries, try fallback method
        logging.warning("All pytube attempts failed, trying fallback method")
        fallback_info = fallback_video_info(video_id)
        if fallback_info:
            return fallback_info
            
        logging.error("Both pytube and fallback methods failed")
        return None
    except Exception as e:
        logging.error(f"Error getting video info: {e}")
        log_exception(e)
        return None

def format_for_markdown(video_info):
    """Format video information for markdown"""
    if not video_info:
        logging.error("No video information to format")
        return None
    
    logging.info("Formatting video information for markdown")
    template = f"""# [{video_info['title']}]

<div style="display:flex">
<div style="flex:40%">
![Video Thumbnail]({video_info['thumbnail_url']})
</div>
<div style="flex:60%">

## Quick Facts
- **Channel:** {video_info['channel_name']} (Subscribers: {video_info.get('channel_subscribers', 'Unknown')})
- **Published:** {video_info['publish_date']}
- **Captured:** {video_info['capture_date']}
- **Duration:** {video_info['duration']}
- **Views:** {video_info['views']}
- **Likes:** {video_info.get('likes', 'Unknown')}
- **Comments:** {video_info.get('comments', 'Unknown')}
- **Category:** {video_info.get('category', 'Unknown')}
- **Personal Rating:** [Add your rating]

</div>
</div>

## Description
{video_info['description']}

## Hashtags
{video_info.get('hashtags', 'None')}

## Link
[Watch on YouTube](https://youtube.com/watch?v={video_info['video_id']})

## Notes
[Add your personal notes about the video here]

---
"""
    logging.info("Markdown formatting complete")
    return template

def append_to_notes(markdown_content, filename="AINotesDump.md"):
    """Append markdown content to the notes file"""
    try:
        logging.info(f"Attempting to write to {filename}")
        # Create the file if it doesn't exist
        if not os.path.exists(filename):
            logging.info(f"File {filename} does not exist, creating it")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("")
            logging.info("File created")
        
        # Append content to the file
        with open(filename, 'a', encoding='utf-8') as f:
            f.write("\n" + markdown_content)
        
        logging.info(f"Successfully appended video information to {filename}")
        return True
    except Exception as e:
        logging.error(f"Error writing to file: {e}")
        log_exception(e)
        return False

def main():
    logging.info("=== Starting YouTube Notes Generator ===")
    # Get YouTube URL from command line or input
    if len(sys.argv) > 1:
        url = sys.argv[1]
        logging.info(f"URL provided as command line argument: {url}")
    else:
        url = input("Enter YouTube URL: ").strip()
        logging.info(f"URL provided via input prompt: {url}")
    
    logging.info(f"Processing video: {url}")
    
    # Get video information
    video_info = get_video_info(url)
    if not video_info:
        logging.error("Failed to get video information")
        return
    
    # Format for markdown
    markdown_content = format_for_markdown(video_info)
    if not markdown_content:
        logging.error("Failed to format video information")
        return
    
    # Append to notes file
    append_to_notes(markdown_content)
    logging.info("=== Script execution completed ===")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical("Unhandled exception in main")
        log_exception(e)
        sys.exit(1) 