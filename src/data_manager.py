from pathlib import Path
from typing import Dict
import json
from datetime import datetime, timedelta


class DataManager:
    """
    Class for managing contact information, inquiries and space availability.
    """

    def __init__(self, json_path: str = "inquiries.json", calendar_path: str = "calendar.json"):
        self.json_path = Path(json_path)
        self.calendar_path = Path(calendar_path)
        self._inquiries = []
        self._calendar = {
            "dvorana": {},  # {date_str: [(start_time, end_time)]}
            "sala_za_sastanke": {},
            "ured": {}
        }
        
        if self.json_path.exists():
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self._inquiries = json.load(f)
                
        if self.calendar_path.exists():
            with open(self.calendar_path, 'r', encoding='utf-8') as f:
                self._calendar = json.load(f)

    def _save_calendar(self):
        """Save calendar data to JSON file."""
        with open(self.calendar_path, 'w', encoding='utf-8') as f:
            json.dump(self._calendar, f, indent=2, ensure_ascii=False)

    def check_availability(self, space_type: str, date: str, start_time: str, end_time: str) -> bool:
        """
        Check if a space is available for the given time slot.
        
        Args:
            space_type: 'dvorana', 'sala_za_sastanke', or 'ured'
            date: Date in YYYY-MM-DD format
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
            
        Returns:
            bool: True if space is available, False otherwise
        """
        if space_type not in self._calendar:
            return False
            
        # Convert times to datetime objects for comparison
        start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
        
        # Get existing bookings for the date
        date_bookings = self._calendar[space_type].get(date, [])
        
        # Check for overlaps with existing bookings
        for booking_start, booking_end in date_bookings:
            booking_start_dt = datetime.strptime(f"{date} {booking_start}", "%Y-%m-%d %H:%M")
            booking_end_dt = datetime.strptime(f"{date} {booking_end}", "%Y-%m-%d %H:%M")
            
            # Check if there's an overlap
            if not (end_dt <= booking_start_dt or start_dt >= booking_end_dt):
                return False
                
        return True

    def add_dummy_bookings(self):
        """Add dummy bookings for the next 30 days for testing purposes."""
        # Generate dates for the next 30 days
        dates = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
        
        for date in dates:
            # Add random bookings with different patterns for each day
            if int(date[-2:]) % 2 == 0:  # Even days
                self._calendar["dvorana"][date] = [("09:00", "12:00"), ("14:00", "17:00")]
                self._calendar["sala_za_sastanke"][date] = [("10:00", "11:00"), ("15:00", "16:30")]
                self._calendar["ured"][date] = [("09:00", "17:00")]
            else:  # Odd days
                self._calendar["dvorana"][date] = [("13:00", "18:00")]
                self._calendar["sala_za_sastanke"][date] = [("09:00", "10:30"), ("14:00", "15:00")]
        
        self._save_calendar()

    def collect_contact(
        self,
        name: str,
        contact_type: str,
        contact_value: str,
        space_type: str,
        requirements: Dict,
    ) -> str:
        """Store contact information and requirements for follow-up."""
        inquiry = {
            "timestamp": datetime.now().isoformat(),
            "name": name,
            "contact_type": contact_type,
            "contact_value": contact_value,
            "space_type": space_type,
            "requirements": requirements,
        }
        
        self._inquiries.append(inquiry)
        
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self._inquiries, f, indent=2, ensure_ascii=False)
        
        return "Hvala na upitu! Kontaktirat ćemo Vas uskoro s ponudom."
