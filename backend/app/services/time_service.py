"""Time Service for handling time-related queries"""
from datetime import datetime
from typing import Dict
import pytz


class TimeService:
    """Service for time-related operations"""
    
    def __init__(self, timezone: str = 'Asia/Ho_Chi_Minh'):
        """Initialize time service
        
        Args:
            timezone: Timezone string (default: Vietnam timezone)
        """
        self.timezone = pytz.timezone(timezone)
    
    def get_current_time(self) -> Dict[str, str]:
        """Get current time in configured timezone
        
        Returns:
            Dictionary with time information
        """
        now = datetime.now(self.timezone)
        
        return {
            "time": now.strftime("%H:%M:%S"),
            "date": now.strftime("%Y-%m-%d"),
            "day_of_week": now.strftime("%A"),
            "timezone": str(self.timezone),
            "formatted": now.strftime("%H:%M:%S, %d/%m/%Y"),
            "vietnamese": self._format_vietnamese(now)
        }
    
    def _format_vietnamese(self, dt: datetime) -> str:
        """Format datetime in Vietnamese
        
        Args:
            dt: Datetime object
            
        Returns:
            Vietnamese formatted string
        """
        days_vi = {
            'Monday': 'Thứ Hai',
            'Tuesday': 'Thứ Ba',
            'Wednesday': 'Thứ Tư',
            'Thursday': 'Thứ Năm',
            'Friday': 'Thứ Sáu',
            'Saturday': 'Thứ Bảy',
            'Sunday': 'Chủ Nhật'
        }
        
        day_name = dt.strftime("%A")
        day_vi = days_vi.get(day_name, day_name)
        
        return f"{day_vi}, {dt.strftime('%d/%m/%Y, %H:%M:%S')}"
