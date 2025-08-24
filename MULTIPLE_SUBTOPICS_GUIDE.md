# Example of Multiple Subtopics Feature for GameContent

## Overview
The GameContent model now supports multiple subtopics with their own information, just like in a handbook format.

## How it works:

### 1. Primary Subtopic
- **Field**: `subtopic` (CharField)
- **Info**: `info` (TextField)
- **Purpose**: The main subtopic and its content

### 2. Additional Subtopics
- **Field**: `subtopics_data` (JSONField)
- **Format**: List of dictionaries with 'subtopic' and 'info' keys
- **Purpose**: Multiple additional subtopics with their own content

## Admin Interface Features:

### Manual Input Fields:
1. **Language**: Choose from English, Kinyarwanda, French, or Swahili
2. **Age Group**: Select from 10-14, 15-19, 20-24, or 25+
3. **Topic**: Enter main topic (like a title)
4. **Subtopic**: Enter main subtopic (like a subtitle)
5. **Info**: Enter main content information

### Multiple Subtopics Section:
- **Add Subtopic Button**: Dynamically adds new subtopic forms
- **Subtopic Name Field**: Text input for subtopic name
- **Subtopic Information Field**: Textarea for detailed content
- **Remove Button**: Removes individual subtopics
- **Auto-save**: JavaScript automatically saves data to hidden field

## Example Usage:

### Topic: "Rwanda History"
#### Primary Subtopic: "Independence Era"
Info: "Rwanda gained independence on July 1, 1962, from Belgium..."

#### Additional Subtopics:
1. **Subtopic**: "Pre-Colonial Period"
   **Info**: "Before colonial rule, Rwanda was organized into kingdoms..."

2. **Subtopic**: "Colonial Period"
   **Info**: "German colonial rule began in 1897, followed by Belgian rule..."

3. **Subtopic**: "Post-Independence Developments"
   **Info**: "After independence, Rwanda faced various political challenges..."

## API Response Format:

```json
{
  "id": 1,
  "topic": "Rwanda History",
  "subtopic": "Independence Era",
  "info": "Rwanda gained independence on July 1, 1962...",
  "all_subtopics": [
    {
      "subtopic": "Independence Era",
      "info": "Rwanda gained independence on July 1, 1962...",
      "is_primary": true
    },
    {
      "subtopic": "Pre-Colonial Period",
      "info": "Before colonial rule, Rwanda was organized...",
      "is_primary": false
    },
    {
      "subtopic": "Colonial Period",
      "info": "German colonial rule began in 1897...",
      "is_primary": false
    }
  ],
  "subtopics_count": 3,
  "language": "english",
  "age_group": "15-19"
}
```

## Benefits:

1. **Handbook-like Structure**: Mimics traditional educational handbooks
2. **Flexible Content**: Each subtopic can have its own detailed information
3. **Easy Management**: Simple UI to add/remove subtopics
4. **API Ready**: Full API support for frontend applications
5. **Searchable**: All subtopic content is searchable
6. **Scalable**: No limit on number of subtopics per topic

## How to Use in Admin:

1. Go to Admin → Game Content → Add Game Content
2. Fill in the required fields (Language, Age Group, Topic, Subtopic, Info)
3. Scroll to "Multiple Subtopics" section
4. Click "Add Subtopic" button
5. Fill in subtopic name and information
6. Repeat for as many subtopics as needed
7. Save the content

The system will automatically handle the data structure and make it available through both the admin interface and API endpoints.
