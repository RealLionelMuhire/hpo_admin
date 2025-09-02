#!/usr/bin/env python3
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hpo.settings')
django.setup()

from hpo_app.models import Question

# Check questions
questions = Question.objects.all()
print(f'Total questions: {questions.count()}')

if questions.exists():
    languages = set(q.language for q in questions)
    print(f'Languages found: {languages}')
    
    print('\nFirst few questions:')
    for q in questions[:3]:
        print(f'  ID: {q.id}, Language: {q.language}, Question: {q.question_text[:50]}...')
        
    # Count by language
    print('\nLanguage distribution:')
    from collections import Counter
    language_counts = Counter(q.language for q in questions)
    for lang, count in language_counts.items():
        print(f'  {lang}: {count} questions')
else:
    print('No questions found in database')
