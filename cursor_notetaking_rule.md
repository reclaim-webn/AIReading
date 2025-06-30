# YouTube Note-Taking Rules

## Purpose
This document outlines the rules for capturing information about YouTube videos related to AI in the AINotesDump.md file.

## Process
When the user shares a YouTube link, the Cursor Agent will:
1. Extract information from the video
2. Format it according to the template below
3. Append it to AINotesDump.md

## Information to Capture

### Required Information
1. Title
2. Thumbnail image
3. Description
4. Link to video
5. Publication date on YouTube
6. Date captured in AINotesDump.md
7. View count
8. Like count
9. Hashtags

### Additional Information
1. Channel name and subscriber count
2. Video duration/length
3. Comment count
4. Category/topic of the video
5. Personal rating/notes about the video

## Format Template

```markdown
# [Video Title]

<div style="display:flex">
<div style="flex:40%">
![Video Thumbnail](thumbnail_url)
</div>
<div style="flex:60%">

## Quick Facts
- **Channel:** Channel name (Subscribers)
- **Published:** YYYY-MM-DD
- **Captured:** YYYY-MM-DD
- **Duration:** HH:MM:SS
- **Views:** 123,456
- **Likes:** 12,345
- **Comments:** 1,234
- **Category:** AI/Machine Learning/etc.
- **Personal Rating:** ★★★★☆

</div>
</div>

## Description
The video description text goes here...

## Hashtags
#AI #MachineLearning #etc

## Link
[Watch on YouTube](https://youtube.com/watch?v=...)

## Notes
Your personal notes about the video...

---
```

## Implementation
The Cursor Agent will handle the extraction and formatting automatically whenever a YouTube link is shared.
