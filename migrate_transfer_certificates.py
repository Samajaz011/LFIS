
import sqlite3
import os
from datetime import datetime

def migrate_transfer_certificates():
    db_path = os.path.join('instance', 'school.db')
    
    if not os.path.exists(db_path):
        print("Database file not found. Creating new database.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transfer_certificate'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("Creating transfer_certificate table...")
            cursor.execute('''
                CREATE TABLE transfer_certificate (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admission_number VARCHAR(20) NOT NULL UNIQUE,
                    file_path VARCHAR(200) NOT NULL,
                    filename VARCHAR(200) NOT NULL,
                    is_issued BOOLEAN NOT NULL DEFAULT 1,
                    uploaded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        else:
            print("transfer_certificate table already exists.")
            
            # Get current table structure
            cursor.execute("PRAGMA table_info(transfer_certificate)")
            columns_info = cursor.fetchall()
            columns = [column[1] for column in columns_info]
            
            print(f"Current columns: {columns}")
            
            # Check if we need to recreate the table with correct structure
            required_columns = ['id', 'admission_number', 'file_path', 'filename', 'is_issued', 'uploaded_at']
            
            # If there are unexpected columns or missing required ones, recreate table
            unexpected_columns = [col for col in columns if col not in required_columns]
            missing_columns = [col for col in required_columns if col not in columns]
            
            if unexpected_columns or missing_columns:
                print(f"Unexpected columns: {unexpected_columns}")
                print(f"Missing columns: {missing_columns}")
                print("Recreating table with correct structure...")
                
                # Backup existing data if any
                cursor.execute("SELECT * FROM transfer_certificate")
                existing_data = cursor.fetchall()
                
                # Drop and recreate table
                cursor.execute("DROP TABLE transfer_certificate")
                cursor.execute('''
                    CREATE TABLE transfer_certificate (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        admission_number VARCHAR(20) NOT NULL UNIQUE,
                        file_path VARCHAR(200) NOT NULL,
                        filename VARCHAR(200) NOT NULL,
                        is_issued BOOLEAN NOT NULL DEFAULT 1,
                        uploaded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Try to restore compatible data
                for row in existing_data:
                    try:
                        if len(row) >= 2:  # At least id and admission_number
                            cursor.execute('''
                                INSERT INTO transfer_certificate 
                                (admission_number, file_path, filename, is_issued, uploaded_at) 
                                VALUES (?, ?, ?, ?, ?)
                            ''', (
                                row[1] if len(row) > 1 else 'unknown',  # admission_number
                                row[2] if len(row) > 2 else '',  # file_path
                                row[3] if len(row) > 3 else 'unknown.pdf',  # filename
                                row[4] if len(row) > 4 else 1,  # is_issued
                                row[5] if len(row) > 5 else datetime.now().isoformat()  # uploaded_at
                            ))
                    except Exception as restore_error:
                        print(f"Could not restore row {row}: {restore_error}")
                        continue
            else:
                print("Table structure is correct.")
        
        conn.commit()
        print("Transfer certificates table migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_transfer_certificates()
