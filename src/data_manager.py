import polars as pl
from pathlib import Path
from typing import Optional


class DataManager:
    def __init__(self, csv_path: str = "src/hall_reservation_schedule.csv"):
        self.csv_path = Path(csv_path)
        self._df: Optional[pl.DataFrame] = None

    def load_data(self) -> None:
        """Load data from CSV file."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at {self.csv_path}")
        self._df = pl.read_csv(self.csv_path)

    def check_availability(
        self, date: str, start_hour: int, end_hour: int
    ) -> pl.DataFrame:
        """Check hall availability for given date and time range."""
        if self._df is None:
            self.load_data()

        start_time = f"{start_hour:02d}:00:00.000000000"
        end_time = f"{end_hour:02d}:00:00.000000000"

        return self._df.filter(
            (pl.col("Date") == date)
            & (pl.col("Start Time") >= start_time)
            & (pl.col("End Time") <= end_time)
        )


# Usage example:
if __name__ == "__main__":
    manager = DataManager()
    result = manager.check_availability("2024-11-12", 10, 13)
    print(f"Available slots:\n{result}")
