#!/usr/bin/env python3
"""
YouTube Notes Generator
This script extracts information from YouTube videos and appends it to AINotesDump.md
"""

import os
import re
import sys
import datetime
from urllib.parse import urlparse, parse_qs
import requests
import json

try:
    from pytube import YouTube
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytube"])
    from pytube import YouTube

def extract_video_id(url):
    """Extract the video ID from a YouTube URL"""
    # Handle different URL formats
    if 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0]
    
    parsed_url = urlparse(url)
    if 'youtube.com' in parsed_url.netloc:
        if '/watch' in parsed_url.path:
            return parse_qs(parsed_url.query)['v'][0]
        elif '/embed/' in parsed_url.path:
            return parsed_url.path.split('/')[-1]
        elif '/v/' in parsed_url.path:
            return parsed_url.path.split('/')[-1]
    
    # If no video ID found, return the original URL (might be just the ID)
    return url

def get_video_info(url):
    """Get information about a YouTube video"""
    try:
        video_id = extract_video_id(url)
        try:
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        except Exception as e:
            print(f"YouTube connection error: {e}")
            print("This may be due to YouTube blocking automated requests or pytube needing an update.")
            return None
        
        # Basic video information
        info = {
            'title': yt.title,
            'channel_name': yt.author,
            'thumbnail_url': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            'description': yt.description,
            'publish_date': yt.publish_date.strftime('%Y-%m-%d') if yt.publish_date else 'Unknown',
            'views': f"{yt.views:,}",
            'video_id': video_id,
            'duration': str(datetime.timedelta(seconds=yt.length)),
            'capture_date': datetime.datetime.now().strftime('%Y-%m-%d'),
        }
        
        # Try to get additional information that may not always be available
        try:
            # Get subscriber count - this requires additional API access
            info['channel_subscribers'] = 'Unknown'  # Requires YouTube API with keys
            
            # Extract hashtags from description
            hashtags = re.findall(r'#\w+', yt.description)
            info['hashtags'] = ' '.join(hashtags) if hashtags else 'None'
            
            # This requires YouTube API with keys for accurate data
            info['likes'] = 'Unknown'  # Requires YouTube API
            info['comments'] = 'Unknown'  # Requires YouTube API
            info['category'] = 'Unknown'  # Requires YouTube API
        except Exception as e:
            print(f"Warning: Could not get all extended information: {e}")
        
        return info
    except Exception as e:
        print(f"Error getting video info: {e}")
        return None

def format_for_markdown(video_info):
    """Format video information for markdown"""
    if not video_info:
        return None
    
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
    return template

def append_to_notes(markdown_content, filename="AINotesDump.md"):
    """Append markdown content to the notes file"""
    try:
        # Create the file if it doesn't exist
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("")
        
        # Append content to the file
        with open(filename, 'a', encoding='utf-8') as f:
            f.write("\n" + markdown_content)
        
        print(f"Successfully appended video information to {filename}")
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False

def main():
    # Get YouTube URL from command line or input
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter YouTube URL: ").strip()
    
    print(f"Processing video: {url}")
    
    # Get video information
    video_info = get_video_info(url)
    if not video_info:
        print("Failed to get video information.")
        return
    
    # Format for markdown
    markdown_content = format_for_markdown(video_info)
    if not markdown_content:
        print("Failed to format video information.")
        return
    
    # Append to notes file
    append_to_notes(markdown_content)

if __name__ == "__main__":
    main() 