"""Knowledge Base Service for CSV file handling"""
import pandas as pd
from typing import List, Dict, Optional
import io
import aiofiles


class KnowledgeService:
    """Service for managing knowledge base from CSV files"""
    
    def __init__(self):
        self.knowledge_data: Optional[pd.DataFrame] = None
        self.csv_content: Optional[str] = None
        
    async def load_csv(self, file_content: bytes, filename: str) -> bool:
        """Load CSV file into knowledge base
        
        Args:
            file_content: CSV file content as bytes
            filename: Name of the uploaded file
            
        Returns:
            Success status
        """
        try:
            # Convert bytes to string
            csv_string = file_content.decode('utf-8')
            self.csv_content = csv_string
            
            # Load into pandas DataFrame
            self.knowledge_data = pd.read_csv(io.StringIO(csv_string))
            
            print(f"Loaded CSV: {filename} with {len(self.knowledge_data)} rows")
            return True
            
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return False
    
    def get_csv_content(self) -> Optional[str]:
        """Get raw CSV content
        
        Returns:
            CSV content as string or None
        """
        return self.csv_content
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search knowledge base
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching records
        """
        if self.knowledge_data is None:
            return []
        
        try:
            # Simple text search across all columns
            query_lower = query.lower()
            
            # Create a mask for rows containing the query
            mask = self.knowledge_data.apply(
                lambda row: any(
                    query_lower in str(val).lower() 
                    for val in row.values
                ), 
                axis=1
            )
            
            results = self.knowledge_data[mask].head(limit)
            return results.to_dict('records')
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics
        
        Returns:
            Statistics dictionary
        """
        if self.knowledge_data is None:
            return {"loaded": False}
        
        return {
            "loaded": True,
            "rows": len(self.knowledge_data),
            "columns": len(self.knowledge_data.columns),
            "column_names": list(self.knowledge_data.columns)
        }
