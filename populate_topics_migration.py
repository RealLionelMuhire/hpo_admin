#!/usr/bin/env python3
"""
Script to populate default topics and subtopics, then migrate existing GameContent
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hpo.settings')
django.setup()

from hpo_app.models import Topic, Subtopic, GameContent

def create_default_topics_and_subtopics():
    """Create default topics and subtopics for existing content"""
    
    # Create default topics for multiple languages
    topics_data = [
        {
            'name': 'General Knowledge',
            'language': 'english',
            'description': 'General knowledge and educational content',
            'subtopics': [
                {'name': 'Educational', 'description': 'General educational content'},
                {'name': 'Fun Facts', 'description': 'Interesting fun facts'},
                {'name': 'Trivia', 'description': 'Trivia questions and facts'},
                {'name': 'Cultural', 'description': 'Cultural knowledge and traditions'},
                {'name': 'Historical', 'description': 'Historical facts and events'},
                {'name': 'Scientific', 'description': 'Scientific knowledge and discoveries'},
            ]
        },
        {
            'name': 'Ubumenyi Rusange',
            'language': 'kinyarwanda',
            'description': 'Ubumenyi rusange n\'amahugurwa',
            'subtopics': [
                {'name': 'Amahugurwa', 'description': 'Ibirimo by\'amahugurwa'},
                {'name': 'Amakuru ashimishije', 'description': 'Amakuru ashimishije n\'atangaje'},
                {'name': 'Ikibazo n\'igisubizo', 'description': 'Ibibazo n\'ibisubizo'},
                {'name': 'Umuco', 'description': 'Umuco n\'imigenzo'},
                {'name': 'Amateka', 'description': 'Amateka n\'ibintu byabaye'},
                {'name': 'Siyanse', 'description': 'Ubumenyi bwa siyanse'},
            ]
        },
        {
            'name': 'Connaissances Générales',
            'language': 'french',
            'description': 'Connaissances générales et contenu éducatif',
            'subtopics': [
                {'name': 'Éducationnel', 'description': 'Contenu éducatif général'},
                {'name': 'Faits Amusants', 'description': 'Faits intéressants et amusants'},
                {'name': 'Culture', 'description': 'Connaissances culturelles'},
                {'name': 'Histoire', 'description': 'Faits et événements historiques'},
                {'name': 'Science', 'description': 'Connaissances scientifiques'},
            ]
        },
        {
            'name': 'Maarifa ya Jumla',
            'language': 'swahili',
            'description': 'Maarifa ya jumla na maudhui ya kielimu',
            'subtopics': [
                {'name': 'Kielimu', 'description': 'Maudhui ya kielimu'},
                {'name': 'Mambo ya Kufurahisha', 'description': 'Mambo ya kufurahisha'},
                {'name': 'Utamaduni', 'description': 'Maarifa ya kitamaduni'},
                {'name': 'Historia', 'description': 'Historia na matukio'},
                {'name': 'Sayansi', 'description': 'Maarifa ya kisayansi'},
            ]
        }
    ]
    
    created_topics = {}
    created_subtopics = {}
    
    for topic_data in topics_data:
        # Create or get topic
        topic, created = Topic.objects.get_or_create(
            name=topic_data['name'],
            language=topic_data['language'],
            defaults={
                'description': topic_data['description']
            }
        )
        created_topics[topic_data['language']] = topic
        print(f"{'Created' if created else 'Found'} topic: {topic}")
        
        # Create subtopics
        for subtopic_data in topic_data['subtopics']:
            subtopic, created = Subtopic.objects.get_or_create(
                topic=topic,
                name=subtopic_data['name'],
                defaults={
                    'description': subtopic_data['description']
                }
            )
            key = f"{topic_data['language']}_{subtopic_data['name'].lower().replace(' ', '_')}"
            created_subtopics[key] = subtopic
            print(f"  {'Created' if created else 'Found'} subtopic: {subtopic}")
    
    return created_topics, created_subtopics

def migrate_existing_content(created_topics, created_subtopics):
    """Migrate existing GameContent to use subtopics"""
    
    # Get all existing GameContent without subtopic
    existing_content = GameContent.objects.filter(subtopic__isnull=True)
    print(f"\nFound {existing_content.count()} existing content items to migrate")
    
    for content in existing_content:
        # Try to determine the best subtopic based on content_type
        language = 'english'  # Default language for existing content
        
        # Map content types to subtopic keys
        content_type_mapping = {
            'educational': 'educational',
            'fun_fact': 'fun_facts',
            'trivia': 'trivia',
            'cultural': 'cultural',
            'historical': 'historical',
            'scientific': 'scientific',
            'general': 'educational',
        }
        
        subtopic_name = content_type_mapping.get(content.content_type, 'educational')
        subtopic_key = f"{language}_{subtopic_name}"
        
        # Get the appropriate subtopic
        if subtopic_key in created_subtopics:
            subtopic = created_subtopics[subtopic_key]
        else:
            # Fallback to first educational subtopic
            subtopic = created_subtopics[f"{language}_educational"]
        
        # Update the content
        content.subtopic = subtopic
        content.save()
        
        print(f"Migrated content '{content.title}' to {subtopic}")

def main():
    print("Creating default topics and subtopics...")
    created_topics, created_subtopics = create_default_topics_and_subtopics()
    
    print("\nMigrating existing content...")
    migrate_existing_content(created_topics, created_subtopics)
    
    print("\nMigration completed successfully!")
    
    # Print summary
    print(f"\nSummary:")
    print(f"Topics created: {Topic.objects.count()}")
    print(f"Subtopics created: {Subtopic.objects.count()}")
    print(f"GameContent items: {GameContent.objects.count()}")
    print(f"GameContent with subtopic: {GameContent.objects.filter(subtopic__isnull=False).count()}")

if __name__ == '__main__':
    main()
