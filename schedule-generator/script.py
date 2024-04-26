import json
import random
from collections import defaultdict

def generate_schedule(json_availability, weeks, days_per_week=5):
    availability = json.loads(json_availability)
    total_spots = weeks * days_per_week
    people = {person for day in availability for person in availability[day]}
    max_appearances = total_spots // len(people)
    
    week_days = ['mon', 'tue', 'wed', 'thu', 'fri']
    week_day_availability = {day: set(availability[day]) for day in week_days}

    day_specific_assignments = {day: defaultdict(int) for day in week_days}

    # Function to generate a week's schedule
    def generate_week():
        weekly_schedule = []
        for day in week_days:
            possible_candidates = [p for p in week_day_availability[day] if total_assignments[p] < max_appearances and p not in weekly_schedule]
            if not possible_candidates:
                raise ValueError("No valid candidates available")
            # Increase weight for candidates based on prior assignments to the same day
            weighted_candidates = sorted(possible_candidates, key=lambda x: (-day_specific_assignments[day][x], total_assignments[x]))
            selected = random.choice(weighted_candidates[:max(2, len(weighted_candidates) // 2)])
            weekly_schedule.append(selected)
            total_assignments[selected] += 1
            day_specific_assignments[day][selected] += 1  # Increase the day-specific count
        return weekly_schedule

    # Try generating the full schedule, retry if it fails
    valid_schedule = False
    while not valid_schedule:
        try:
            total_assignments = {person: 0 for person in people}
            for day in week_days:
                day_specific_assignments[day] = defaultdict(int)
            all_weeks_schedule = []
            for week in range(weeks):
                week_schedule = generate_week()
                all_weeks_schedule.append(week_schedule)
            valid_schedule = True
        except ValueError:
            continue  # Retry if schedule generation failed

    # Print the valid schedule
    for week, schedule in enumerate(all_weeks_schedule, 1):
        print(f"Week {week}: {', '.join(schedule)}")

json_availability = input("Enter availability as JSON: ")
amount_of_people = len(set([person for day in json.loads(json_availability) for person in json.loads(json_availability)[day]]))
print(f"Amount of people: {amount_of_people}")

generate_schedule(json_availability, weeks=amount_of_people)
