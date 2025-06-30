# YouTube Notes Generator

This tool extracts information from YouTube videos and appends it to `AINotesDump.md` following a consistent format.

## Features

- Extracts video title, channel name, description, and other metadata
- Formats information in a clean, readable Markdown format
- Automatically installs required dependencies
- Handles various YouTube URL formats
- Extracts hashtags from the video description

## Setup

1. Make sure you have Python 3.6 or higher installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

You can use the script in two ways:

### Method 1: Run and enter URL

```bash
python youtube_notes.py
```

Then enter the YouTube URL when prompted.

### Method 2: Pass URL as argument

```bash
python youtube_notes.py "https://www.youtube.com/watch?v=qWm8yJ_mDAs"
```

## Output

The script will:
1. Extract information from the YouTube video
2. Format it according to the template in `cursor_notetaking_rule.md`
3. Append it to `AINotesDump.md`

## Limitations

Some information (likes, comments, subscriber count) requires YouTube API access with an API key. These fields will show as "Unknown" in the output.

## Example

Processing a video will add an entry to `AINotesDump.md` that looks like:

```markdown
# [Video Title]

<div style="display:flex">
<div style="flex:40%">
![Video Thumbnail](thumbnail_url)
</div>
<div style="flex:60%">

## Quick Facts
- **Channel:** Channel name (Subscribers: Unknown)
- **Published:** YYYY-MM-DD
- **Captured:** YYYY-MM-DD
- **Duration:** HH:MM:SS
- **Views:** 123,456
- **Likes:** Unknown
- **Comments:** Unknown
- **Category:** Unknown
- **Personal Rating:** [Add your rating]

</div>
</div>

## Description
The video description text goes here...

## Hashtags
#hashtag1 #hashtag2

## Link
[Watch on YouTube](https://youtube.com/watch?v=VIDEO_ID)

## Notes
[Add your personal notes about the video here]

---
``` 