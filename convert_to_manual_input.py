#!/usr/bin/env python3
"""
Data migration script to convert GameContent from hierarchical to manual input structure
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/home/leo/hpo/hpo_django/hpo_admin')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hpo.settings')
django.setup()

from hpo_app.models import GameContent, Topic, Subtopic

def convert_existing_content():
    """Convert existing GameContent to use manual input fields"""
    print("Converting existing GameContent to manual input structure...")
    
    # Get all GameContent records
    content_records = GameContent.objects.all()
    
    updated_count = 0
    for content in content_records:
        # Check if this content needs conversion (has numeric subtopic value)
        try:
            # If subtopic is a number (string representation of ID), convert it
            if content.subtopic and content.subtopic.isdigit():
                subtopic_id = int(content.subtopic)
                try:
                    # Get the actual Subtopic and Topic objects
                    old_subtopic = Subtopic.objects.get(id=subtopic_id)
                    old_topic = old_subtopic.topic
                    
                    # Update the content with manual input fields
                    content.language = old_topic.language
                    content.topic = old_topic.name
                    content.subtopic = old_subtopic.name
                    
                    # Ensure age_group is set (it should already be)
                    if not content.age_group:
                        content.age_group = '15-19'  # Default value
                    
                    content.save()
                    updated_count += 1
                    print(f"Updated content: {content.topic} → {content.subtopic} ({content.language})")
                    
                except Subtopic.DoesNotExist:
                    print(f"Warning: Could not find subtopic with ID {subtopic_id} for content {content.id}")
                    # Set default values
                    content.language = 'english'
                    content.topic = 'General'
                    content.subtopic = 'General Knowledge'
                    if not content.age_group:
                        content.age_group = '15-19'
                    content.save()
                    updated_count += 1
                    
            else:
                # Content might already be converted or needs default values
                if not content.language:
                    content.language = 'english'
                if not content.topic:
                    content.topic = 'General'
                if not content.subtopic:
                    content.subtopic = 'General Knowledge'
                if not content.age_group:
                    content.age_group = '15-19'
                content.save()
                updated_count += 1
                print(f"Set defaults for content: {content.topic} → {content.subtopic} ({content.language})")
                
        except (ValueError, TypeError) as e:
            print(f"Error processing content {content.id}: {e}")
            # Set default values
            content.language = 'english'
            content.topic = 'General'
            content.subtopic = 'General Knowledge'
            if not content.age_group:
                content.age_group = '15-19'
            content.save()
            updated_count += 1
    
    print(f"Conversion complete! Updated {updated_count} content records.")
    
    # Show summary
    total_content = GameContent.objects.count()
    print(f"Total content records: {total_content}")
    
    # Show distribution by language
    print("\nContent distribution by language:")
    for lang_code, lang_name in GameContent.LANGUAGE_CHOICES:
        count = GameContent.objects.filter(language=lang_code).count()
        print(f"  {lang_name}: {count}")

if __name__ == '__main__':
    convert_existing_content()
