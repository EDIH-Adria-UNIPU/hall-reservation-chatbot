import polars as pl
from datetime import date, timedelta
import random

random.seed(42)

start_date = date.today()

# Generate data for 10 days
dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(10)]

time_slots = [f"{hour}:00-{hour+1}:00" for hour in range(8, 20)]  # 8 to 19

schedule = []
for date in dates:
    for time in time_slots:
        # Randomly decide if the hall is taken (30% chance)
        hall = "Taken" if random.random() < 0.3 else "Free"

        # Randomly decide if the room is taken (50% chance)
        room = "Taken" if random.random() < 0.5 else "Free"

        # Randomly decide number of seats taken (0 to 10)
        seats_taken = random.randint(0, 10)

        schedule.append(
            {
                "Date": date,
                "Time Slot": time,
                "Conference Hall": hall,
                "Meeting Room": room,
                "Coworking Seats Taken": seats_taken,
            }
        )

df = pl.DataFrame(schedule)
df = df.sort(["Date", "Time Slot"])
print(df)

df.write_csv("hall_reservation_schedule.csv")
