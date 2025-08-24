from django.core.management.base import BaseCommand
from hpo_app.models import GameContent, Admin
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate sample game content data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate game content...'))
        
        # Sample game content data
        sample_content = [
            {
                'title': 'History of Rwanda',
                'language': 'english',
                'age_group': '15-19',
                'topic': 'History',
                'subtopics': ['Rwanda Independence', 'Colonial Period', 'Pre-colonial Rwanda'],
                'info': 'Rwanda gained independence from Belgium on July 1, 1962. The country has made remarkable progress in unity and development since then.',
                'content_type': 'historical',
                'difficulty_level': 'intermediate',
                'status': 'published',
                'tags': 'rwanda, history, independence, africa',
                'card_association': 'S3'
            },
            {
                'title': 'Amateka y\'u Rwanda',
                'language': 'kinyarwanda',
                'age_group': '15-19',
                'topic': 'Amateka',
                'subtopics': ['Ubwiyunge bw\'u Rwanda', 'Igihe cy\'abakoloni', 'U Rwanda rw\'ubunyangamugayo'],
                'info': 'U Rwanda rwabonye ubwiyunge ku ya 1 Nyakanga 1962. Igihugu cyateye imbere cyane mu kwiyunga no kwiyubakira.',
                'content_type': 'historical',
                'difficulty_level': 'intermediate',
                'status': 'published',
                'tags': 'rwanda, amateka, ubwiyunge, afurika',
                'card_association': 'S3'
            },
            {
                'title': 'Rwandan Culture and Traditions',
                'language': 'english',
                'age_group': '20-24',
                'topic': 'Culture',
                'subtopics': ['Traditional Dances', 'Traditional Music', 'Crafts and Arts', 'Festivals'],
                'info': 'Rwanda has rich cultural traditions including Intore dance, traditional music, and crafts. These traditions are preserved and celebrated throughout the country.',
                'content_type': 'cultural',
                'difficulty_level': 'beginner',
                'status': 'published',
                'tags': 'culture, traditions, dance, intore, music',
                'card_association': 'HJ'
            },
            {
                'title': 'Science and Technology in Rwanda',
                'language': 'english',
                'age_group': '20-24',
                'topic': 'Technology',
                'subtopics': ['Digital Transformation', 'Innovation Hubs', 'ICT Infrastructure', 'Tech Education'],
                'info': 'Rwanda is leading Africa in digital transformation with initiatives like Kigali Innovation City, cashless payments, and widespread internet connectivity.',
                'content_type': 'scientific',
                'difficulty_level': 'advanced',
                'status': 'published',
                'tags': 'technology, innovation, digital, kigali, development',
                'card_association': 'DA'
            },
            {
                'title': 'Wildlife in Rwanda',
                'language': 'english',
                'age_group': '10-14',
                'topic': 'Nature',
                'subtopics': ['Mountain Gorillas', 'National Parks', 'Conservation Efforts', 'Biodiversity'],
                'info': 'Rwanda is home to endangered mountain gorillas in Volcanoes National Park. Conservation efforts have helped increase their population.',
                'content_type': 'educational',
                'difficulty_level': 'beginner',
                'status': 'published',
                'tags': 'wildlife, gorillas, conservation, volcanoes, park',
                'card_association': 'C7'
            },
            {
                'title': 'Ubuzima bw\'inyamaswa mu Rwanda',
                'language': 'kinyarwanda',
                'age_group': '10-14',
                'topic': 'Kamere',
                'subtopics': ['Ingagi z\'umusozi', 'Pariki z\'inyamaswa', 'Kubungabunga kamere', 'Ibinyabuzima bitandukanye'],
                'info': 'U Rwanda rufite ingagi zisanzwe ku misozi mu kibuga cy\'inyamaswa cya Volcanoes. Ibikorwa byo kubungabunga byatumye ubwiyongere bwazo.',
                'content_type': 'educational',
                'difficulty_level': 'beginner',
                'status': 'published',
                'tags': 'inyamaswa, ingagi, kubungabunga, volcanoes, pariki',
                'card_association': 'C7'
            },
            {
                'title': 'Sports in Rwanda',
                'language': 'english',
                'age_group': '15-19',
                'topic': 'Sports',
                'subtopics': ['Football', 'Basketball', 'Cycling', 'Athletics'],
                'info': 'Football and basketball are very popular in Rwanda. The country has professional leagues and participates in international competitions.',
                'content_type': 'general',
                'difficulty_level': 'beginner',
                'status': 'published',
                'tags': 'sports, football, basketball, competitions, leagues',
                'card_association': 'H9'
            },
            {
                'title': 'Mathematics Fun Facts',
                'language': 'english',
                'age_group': '25+',
                'topic': 'Mathematics',
                'subtopics': ['Number Theory', 'Mathematical Constants', 'Famous Mathematicians', 'Mathematical Puzzles'],
                'info': 'Did you know that the number 1729 is known as the Hardy-Ramanujan number? It\'s the smallest number that can be expressed as the sum of two cubes in two different ways.',
                'content_type': 'fun_fact',
                'difficulty_level': 'advanced',
                'status': 'published',
                'tags': 'mathematics, numbers, hardy, ramanujan, cubes',
                'card_association': 'SQ'
            }
        ]
        
        # Get the first admin as creator (if exists)
        creator = Admin.objects.first()
        
        # Create game content
        created_count = 0
        for content_data in sample_content:
            content_data['created_by'] = creator
            if content_data['status'] == 'published':
                content_data['published_at'] = timezone.now()
                content_data['approved_by'] = creator
            
            content, created = GameContent.objects.get_or_create(
                title=content_data['title'],
                language=content_data['language'],
                defaults=content_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {content.title} ({content.language})')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Already exists: {content.title} ({content.language})')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new game content items.')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total game content in database: {GameContent.objects.count()}')
        )
