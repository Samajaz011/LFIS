
from app import app, db
from models import Banner

def migrate_banner_table():
    with app.app_context():
        # Add new columns to existing banner table
        try:
            # Check if columns exist, if not add them
            with db.engine.connect() as conn:
                # Add image_url column
                try:
                    conn.execute(db.text("ALTER TABLE banner ADD COLUMN image_url VARCHAR(200)"))
                    print("Added image_url column")
                except Exception as e:
                    print(f"image_url column might already exist: {e}")
                
                # Add order_index column
                try:
                    conn.execute(db.text("ALTER TABLE banner ADD COLUMN order_index INTEGER DEFAULT 0"))
                    print("Added order_index column")
                except Exception as e:
                    print(f"order_index column might already exist: {e}")
                
                # Update banner_type choices to include slider
                try:
                    conn.execute(db.text("UPDATE banner SET banner_type = 'slider' WHERE banner_type NOT IN ('flash', 'popup')"))
                    print("Updated banner types")
                except Exception as e:
                    print(f"Error updating banner types: {e}")
                
                conn.commit()
            
            print("Migration completed successfully!")
            
        except Exception as e:
            print(f"Migration error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    migrate_banner_table()
