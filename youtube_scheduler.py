import random import datetime

Define competitor peak posting hours (for example purposes)

PEAK_HOURS = [ (9, 11),   # Morning traffic (13, 15),  # Early afternoon (18, 21)   # Evening prime time ]

def get_next_best_upload_time(): today = datetime.datetime.now() best_slots = []

for start, end in PEAK_HOURS:
    for hour in range(start, end + 1):
        slot = today.replace(hour=hour, minute=random.randint(0, 59), second=0, microsecond=0)
        if slot > today:
            best_slots.append(slot)

if not best_slots:
    # If all slots for today have passed, pick the earliest slot for tomorrow
    tomorrow = today + datetime.timedelta(days=1)
    start, end = PEAK_HOURS[0]
    slot = tomorrow.replace(hour=start, minute=0, second=0, microsecond=0)
    return slot

return random.choice(best_slots)

if name == "main": print("Next best upload time:", get_next_best_upload_time())

