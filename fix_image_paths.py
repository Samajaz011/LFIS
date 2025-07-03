
import os
import shutil
from app import app, db
from models import Gallery, Faculty, Banner

def fix_image_paths():
    """Fix existing image paths in database"""
    with app.app_context():
        # Fix Gallery images
        gallery_items = Gallery.query.all()
        for item in gallery_items:
            if item.image_url and item.image_url.startswith('/static/uploads/'):
                new_url = item.image_url.replace('/static/uploads/', '/uploads/')
                item.image_url = new_url
                print(f"Fixed gallery image: {item.title} -> {new_url}")
        
        # Fix Faculty images
        faculty_items = Faculty.query.all()
        for item in faculty_items:
            if item.image_url and item.image_url.startswith('/static/uploads/'):
                new_url = item.image_url.replace('/static/uploads/', '/uploads/')
                item.image_url = new_url
                print(f"Fixed faculty image: {item.name} -> {new_url}")
        
        # Fix Banner images
        banner_items = Banner.query.all()
        for item in banner_items:
            if item.image_url and item.image_url.startswith('/static/uploads/'):
                new_url = item.image_url.replace('/static/uploads/', '/uploads/')
                item.image_url = new_url
                print(f"Fixed banner image: {item.title} -> {new_url}")
        
        db.session.commit()
        print("All image paths fixed successfully!")

if __name__ == '__main__':
    fix_image_paths()
