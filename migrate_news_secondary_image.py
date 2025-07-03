
#!/usr/bin/env python3

import sqlite3
import os

def migrate_news_secondary_image():
    db_path = os.path.join('instance', 'school.db')
    
    if not os.path.exists(db_path):
        print("Database file not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if secondary_image_url column already exists
        cursor.execute("PRAGMA table_info(news)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'secondary_image_url' not in columns:
            print("Adding secondary_image_url column to news table...")
            cursor.execute("ALTER TABLE news ADD COLUMN secondary_image_url VARCHAR(200)")
            conn.commit()
            print("Successfully added secondary_image_url column!")
        else:
            print("secondary_image_url column already exists!")
        
        conn.close()
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    migrate_news_secondary_image()
