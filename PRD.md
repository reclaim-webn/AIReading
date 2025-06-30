# YouTube Notes Generator - Product Requirements Document

## 1. Project Overview

This project aims to create a system that automatically extracts and saves information from YouTube videos in a structured format. The system will append the extracted information to a Markdown file (AINotesDump.md) whenever the user provides a YouTube link.

## 2. User Requirements

### 2.1 Core Requirements

The system must capture and store the following information for each YouTube video:

1. Thumbnail image
2. Video description
3. Link to the video
4. Publication date on YouTube
5. Capture date (when the information was added to AINotesDump.md)
6. View count
7. Like count
8. Video title
9. Hashtags

### 2.2 Additional Requirements

The system should also capture these additional data points:

1. Channel name and subscriber count
2. Video duration/length
3. Comment count
4. Category/topic of the video
5. Space for personal rating/notes

### 2.3 Format Requirements

The notes should be formatted with:
- A mix of one-column and two-columnar layout
- Image on the left and facts on the right column
- Consistent, readable formatting
- Clear section headers

## 3. Available Approaches

### 3.1 Manual Approach
**Description:** User manually copies and pastes information from YouTube into a template.

**Pros:**
- No technical setup required
- Works without any API access or dependencies
- Always accurate (human-verified data)

**Cons:**
- Time-consuming
- Prone to human error
- Inconsistent formatting possible

### 3.2 Browser Extension/Bookmarklet
**Description:** A custom browser extension or bookmarklet that extracts information from the current YouTube page.

**Pros:**
- One-click operation
- Access to rendered page content (including dynamically loaded elements)
- Can extract information that may not be available via API

**Cons:**
- Requires browser extension development
- Browser-specific
- May break with YouTube interface changes

### 3.3 YouTube API Approach
**Description:** Use YouTube Data API to fetch video information.

**Pros:**
- Official, structured data access
- Most reliable and comprehensive data
- Handles all edge cases properly

**Cons:**
- Requires API key setup
- Has quota limitations
- Requires server-side implementation

### 3.4 Python Script with pytube Library
**Description:** A Python script that uses the pytube library to extract available video information without requiring API keys.

**Pros:**
- No API key required
- Relatively simple implementation
- Works cross-platform
- Can be run locally

**Cons:**
- Cannot access all data (likes, comments, subscriber count require API)
- May break with YouTube changes
- Requires Python installation

## 4. Selected Approach

**Selected: Python Script with pytube Library**

We selected the Python script approach using the pytube library because it provides a good balance between:
- Ease of implementation
- No need for API keys or quotas
- Access to most critical information
- Local execution without external dependencies
- Minimal setup requirements for the user

While this approach doesn't provide access to all desired information (likes, comment counts, and subscriber counts), it meets the core requirements without requiring API keys or extensive setup.

## 5. Implementation Details

### 5.1 Technology Stack
- Python 3.6+
- pytube library for YouTube data extraction
- requests library for potential future enhancements

### 5.2 Script Functionality
The implemented script (`youtube_notes.py`):
- Extracts video ID from various YouTube URL formats
- Fetches available video metadata using pytube
- Formats the information according to the defined template
- Appends the formatted information to AINotesDump.md
- Handles errors gracefully
- Auto-installs required dependencies if needed

### 5.3 Output Format
The script generates a Markdown entry with:
- Video title as heading
- Two-column layout with thumbnail and quick facts
- Sections for description, hashtags, link, and personal notes
- Divider for separation between entries

## 6. Future Enhancements

Potential future improvements:
1. Add YouTube API integration (optional) for accessing likes, comments, and subscriber counts
2. Create a simple GUI interface
3. Add batch processing for multiple URLs
4. Implement automatic categorization/tagging based on video content
5. Add export to other formats (HTML, PDF)
6. Include video transcript when available 