#!/usr/bin/env python3
"""
YouTube Notes Generator
This script extracts information from YouTube videos and appends it to AINotesDump.md
"""

import os
import re
import sys
import json
import datetime
import traceback
import logging
import subprocess
from urllib.parse import urlparse, parse_qs

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

def ensure_dependencies():
    """Ensure all required dependencies are installed"""
    try:
        logging.info("Checking for required dependencies")
        try:
            import yt_dlp
            logging.info("yt-dlp already installed")
        except ImportError:
            logging.info("Installing yt-dlp")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
            logging.info("Successfully installed yt-dlp")
            import yt_dlp
        
        return True
    except Exception as e:
        logging.error(f"Failed to install dependencies: {e}")
        log_exception(e)
        return False

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

def get_video_info(url):
    """Get information about a YouTube video using yt-dlp"""
    try:
        import yt_dlp
        
        video_id = extract_video_id(url)
        logging.info(f"Getting information for video ID: {video_id}")
        
        # Configure yt-dlp
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,  # We don't want to download the video, just get info
            'ignoreerrors': True,
        }
        
        # Extract video information
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logging.info("Extracting video information with yt-dlp")
            video_info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            
            if not video_info:
                logging.error("yt-dlp couldn't extract video information")
                return None
            
            logging.info(f"Successfully extracted video information: {video_info.get('title')}")
            
            # Format duration
            duration_seconds = video_info.get('duration')
            if duration_seconds:
                duration = str(datetime.timedelta(seconds=duration_seconds))
            else:
                duration = "Unknown"
                
            # Extract hashtags
            description = video_info.get('description', '')
            hashtags = re.findall(r'#\w+', description)
            hashtags_str = ' '.join(hashtags) if hashtags else 'None'
            
            # Create info dictionary
            info = {
                'title': video_info.get('title', f"YouTube Video {video_id}"),
                'channel_name': video_info.get('uploader', 'Unknown'),
                'channel_url': video_info.get('uploader_url', ''),
                'thumbnail_url': video_info.get('thumbnail', f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"),
                'description': description,
                'publish_date': video_info.get('upload_date', 'Unknown'),
                'views': f"{video_info.get('view_count', 0):,}",
                'video_id': video_id,
                'duration': duration,
                'capture_date': datetime.datetime.now().strftime('%Y-%m-%d'),
                'hashtags': hashtags_str,
                'channel_subscribers': video_info.get('channel_follower_count', 'Unknown'),
                'likes': f"{video_info.get('like_count', 0):,}" if video_info.get('like_count') else 'Unknown',
                'comments': f"{video_info.get('comment_count', 0):,}" if video_info.get('comment_count') else 'Unknown',
                'category': video_info.get('categories', ['Unknown'])[0] if video_info.get('categories') else 'Unknown'
            }
            
            # Format publish date to be more readable if it's in YYYYMMDD format
            if len(info['publish_date']) == 8 and info['publish_date'].isdigit():
                try:
                    publish_date = datetime.datetime.strptime(info['publish_date'], '%Y%m%d')
                    info['publish_date'] = publish_date.strftime('%Y-%m-%d')
                except Exception:
                    pass  # Keep original format if parsing fails
                    
            logging.info(f"Processed video information: Title={info['title']}, Channel={info['channel_name']}")
            return info
            
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
    
    # Truncate description if too long
    description = video_info['description']
    if len(description) > 2000:
        description = description[:1997] + "..."
    
    # Build channel name with link if available
    channel_display = video_info['channel_name']
    if video_info.get('channel_url'):
        channel_display = f"[{video_info['channel_name']}]({video_info['channel_url']})"
    
    template = f"""# [{video_info['title']}]

<div style="display:flex">
<div style="flex:40%">
![Video Thumbnail]({video_info['thumbnail_url']})
</div>
<div style="flex:60%">

## Quick Facts
- **Channel:** {channel_display} (Subscribers: {video_info.get('channel_subscribers', 'Unknown')})
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
{description}

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
    
    # Ensure dependencies are installed
    if not ensure_dependencies():
        logging.error("Failed to install required dependencies")
        return
    
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