import polars as pl
from pathlib import Path
from typing import Optional
import warnings


class DataManager:
    """
    Class for reading and filtering hall reservation schedule data.
    """

    def __init__(self, csv_path: str = "hall_reservation_schedule.csv"):
        self.csv_path = Path(csv_path)
        self._df: Optional[pl.DataFrame] = None
        
        if not self.csv_path.exists():
            warnings.warn(f"CSV file not found at {self.csv_path}. Please ensure the file exists before loading data.")

    def load_data(self) -> None:
        """Load data from CSV file."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at {self.csv_path}")
        self._df = pl.read_csv(str(self.csv_path))

    def check_availability(
        self, date: str, start_hour: int, end_hour: int
    ) -> pl.DataFrame:
        """Check hall availability for given date and time range."""
        if self._df is None:
            self.load_data()

        return self._df.filter(
            (pl.col("Date") == date)
            & (pl.col("Start Time") >= start_hour)
            & (pl.col("End Time") <= end_hour)
        )

    def make_reservation(
        self, area_type: str, date: str, start_hour: int, end_hour: int
    ) -> str:
        """Make a reservation for specified area type, date and time range."""
        area_types = ["hall", "room", "coworking"]

        if area_type not in area_types:
            raise ValueError("Invalid area type. Must be 'hall', 'room' or 'coworking'")

        # Dummy implementation
        return f"Reservation successful: {area_type} reserved for {date} from {start_hour:02d}:00 to {end_hour:02d}:00"


# Usage example:
if __name__ == "__main__":
    manager = DataManager()
    result = manager.check_availability("2024-11-13", 10, 13)
    print(f"Available slots:\n{result}")
