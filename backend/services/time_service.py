"""
Time Service - Multiple timezone support
"""
from datetime import datetime
import pytz
from typing import Dict

# Timezone mappings
TIMEZONES = {
    "vietnam": "Asia/Ho_Chi_Minh",
    "vn": "Asia/Ho_Chi_Minh",
    "việt nam": "Asia/Ho_Chi_Minh",
    "nhật bản": "Asia/Tokyo",
    "nhật": "Asia/Tokyo",
    "japan": "Asia/Tokyo",
    "jp": "Asia/Tokyo",
    "hàn quốc": "Asia/Seoul",
    "hàn": "Asia/Seoul",
    "korea": "Asia/Seoul",
    "kr": "Asia/Seoul",
    "mỹ": "America/New_York",
    "usa": "America/New_York",
    "us": "America/New_York",
    "america": "America/New_York",
}

# Vietnamese weekday names
WEEKDAYS_VI = {
    0: "Thứ Hai",
    1: "Thứ Ba",
    2: "Thứ Tư",
    3: "Thứ Năm",
    4: "Thứ Sáu",
    5: "Thứ Bảy",
    6: "Chủ Nhật",
}

# Country flags
FLAGS = {
    "vietnam": "🇻🇳",
    "japan": "🇯🇵",
    "korea": "🇰🇷",
    "usa": "🇺🇸",
}


class TimeService:
    @staticmethod
    def get_time(timezone_name: str = "vietnam") -> Dict:
        """Get current time for specified timezone"""
        # Normalize timezone name
        tz_key = timezone_name.lower().strip()
        
        # Get timezone
        tz_str = TIMEZONES.get(tz_key, TIMEZONES["vietnam"])
        tz = pytz.timezone(tz_str)
        
        # Get current time
        now = datetime.now(tz)
        
        # Format time
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%d/%m/%Y")
        weekday = WEEKDAYS_VI[now.weekday()]
        
        # Determine country for flag
        country = "vietnam"
        if "japan" in tz_key or "nhật" in tz_key or "jp" == tz_key:
            country = "japan"
        elif "korea" in tz_key or "hàn" in tz_key or "kr" == tz_key:
            country = "korea"
        elif "usa" in tz_key or "mỹ" in tz_key or "us" == tz_key or "america" in tz_key:
            country = "usa"
        
        flag = FLAGS.get(country, "🇻🇳")
        
        # Country name in Vietnamese
        country_names = {
            "vietnam": "Việt Nam",
            "japan": "Nhật Bản",
            "korea": "Hàn Quốc",
            "usa": "Mỹ",
        }
        country_name = country_names.get(country, "Việt Nam")
        
        return {
            "time": time_str,
            "date": date_str,
            "weekday": weekday,
            "timezone": country_name,
            "flag": flag
        }
    
    @staticmethod
    def format_time_response(time_info: Dict) -> str:
        """Format time information into response string"""
        return (
            f"⏰ **Bây giờ là {time_info['time']}**, "
            f"{time_info['weekday']} ngày **{time_info['date']}** "
            f"{time_info['flag']} *(giờ {time_info['timezone']})*"
        )


# Global instance
time_service = TimeService()
