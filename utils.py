"""
Utility functions for CKEditor file handling
"""
import os
import uuid
from django.utils.text import slugify


def get_filename(filename):
    """
    Generate a unique filename for uploaded files
    """
    # Get the file extension
    name, ext = os.path.splitext(filename)
    
    # Create a slugified version of the name
    slug_name = slugify(name)
    
    # Generate a unique identifier
    unique_id = str(uuid.uuid4())[:8]
    
    # Combine everything
    new_filename = f"{slug_name}_{unique_id}{ext}"
    
    return new_filename
