import polars as pl
from pathlib import Path
from typing import Optional, Dict
import warnings
import json
from datetime import datetime


class DataManager:
    """
    Class for managing contact information and inquiries.
    """

    def __init__(self, json_path: str = "inquiries.json"):
        self.json_path = Path(json_path)
        self._inquiries = []
        
        if self.json_path.exists():
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self._inquiries = json.load(f)

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
