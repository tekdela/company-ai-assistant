"""
Knowledge Service - CSV/TXT file processing and SQLite storage
"""
import sqlite3
import pandas as pd
import os
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class KnowledgeService:
    def __init__(self, db_path: str = "knowledge.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with knowledge table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_file TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def upload_file(self, file_path: str, filename: str) -> Dict:
        """Process and store CSV/TXT file content"""
        try:
            # Determine file type and read content
            if filename.endswith('.csv'):
                # Try different encodings
                try:
                    df = pd.read_csv(file_path, encoding='utf-8')
                except:
                    try:
                        df = pd.read_csv(file_path, encoding='utf-8-sig')
                    except:
                        df = pd.read_csv(file_path, encoding='latin1')
                
                # Convert dataframe to text records
                records = []
                for idx, row in df.iterrows():
                    record = " | ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
                    records.append(record)
                
            elif filename.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                records = [line.strip() for line in content.split('\n') if line.strip()]
            else:
                return {"success": False, "message": "Unsupported file type"}
            
            # Store in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for record in records:
                cursor.execute(
                    "INSERT INTO knowledge (source_file, content) VALUES (?, ?)",
                    (filename, record)
                )
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "message": f"Đã xử lý thành công {len(records)} records từ {filename}",
                "records_count": len(records)
            }
        
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            return {"success": False, "message": f"Lỗi xử lý file: {str(e)}"}
    
    def search(self, query: str) -> List[Dict]:
        """Search knowledge base for relevant information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Search for records containing any of the query words
            search_terms = query.lower().split()
            results = []
            
            cursor.execute("SELECT DISTINCT content, source_file FROM knowledge")
            all_records = cursor.fetchall()
            
            for content, source_file in all_records:
                content_lower = content.lower()
                # Check if any search term is in the content
                if any(term in content_lower for term in search_terms):
                    results.append({
                        "content": content,
                        "source": source_file
                    })
            
            conn.close()
            return results[:5]  # Return top 5 results
        
        except Exception as e:
            logger.error(f"Error searching knowledge: {str(e)}")
            return []
    
    def get_all_count(self) -> int:
        """Get total number of records in knowledge base"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM knowledge")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0


# Global instance
knowledge_service = KnowledgeService()
