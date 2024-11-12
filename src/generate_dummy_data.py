import polars as pl
from datetime import date, timedelta, time
import random

random.seed(42)

start_date = date.today()
TOTAL_SEATS = 10
DAYS = 10

dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(DAYS)]

time_slots = [(time(hour, 0), time(hour + 1, 0)) for hour in range(8, 20)]  # 8 to 19

schedule = []
for date in dates:
    for start_time, end_time in time_slots:
        hall_free = 1 if random.random() > 0.3 else 0
        room_free = 1 if random.random() > 0.5 else 0
        seats_taken = random.randint(0, 10)
        seats_free = TOTAL_SEATS - seats_taken

        schedule.append(
            {
                "Date": date,
                "Start Time": start_time,
                "End Time": end_time,
                "Conference Hall Available": hall_free,
                "Meeting Room Available": room_free,
                "Coworking Seats Available": seats_free,
            }
        )

df = pl.DataFrame(schedule)
df = df.sort(["Date", "Start Time"])
print(df)

df.write_csv("hall_reservation_schedule.csv")
