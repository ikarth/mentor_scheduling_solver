import os
import sys
import json
import pprint
import numpy
import random

print("""
=== Interpert Solutions ===
Takes the solution the solver finds (in JSON format) and translates it into
a readable format.

Needs to be adjusted if the schedule parameters differ from the original
hardcoded assumption that the scheduling range is Monday through Friday,
9am to 8pm.
"""
)

solution = {}
with open("solution_split_01e.json", "r") as f:
    solution = json.load(f)

team_data = {}
with open("split_01_teams.json", "r") as dzn_json:
    team_data = json.load(dzn_json)

#solution["max_possible_score"] = 100 + 300 + 120
solution["team_assigned_meeting_times"]
solution["team_assigned_mentor"]
solution["mentor_meeting_count"]
solution["team_score"]
solution["overall_score"]
solution["max_possible_score"]

day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
quarter_hour_names = [":00", ":15", ":30", ":45"]
def time_index_to_date(time_index):
    hours = 11 # 4 slots per hour in the time indexing
    day = time_index // (hours * 4)
    slot = time_index % (hours * 4)
    hour_name_digits = 9 + (slot // 4)
    quarter_hour_digits = slot % 4
    quarter_name = quarter_hour_names[quarter_hour_digits]
    postfix = " am"
    if hour_name_digits > 12:
        hour_name_digits -= 12
        postfix = " pm"
    if hour_name_digits == 12:
        if quarter_hour_digits == 0:
            postfix = " noon"
    return f"{day_names[day]}, at {hour_name_digits}{quarter_name}{postfix}.\t[{time_index}]\t"

print(team_data)
print()
print("Schedule for Split 01 (2020F)")
print("=============================")
print()
print(f"Overall solution quality: {solution['overall_score']} / {solution['max_possible_score']}")
print()
print("## Teams")
mentor_schedule_matrix = [[],[],[],[],[],[],[],[],[],[]]

for team_index, team_time in enumerate(solution["team_assigned_meeting_times"]):
    print("---")
    print(f"Team: {team_data['teams'][str(team_index)]}")
    print(time_index_to_date(team_time - 1)) # times are 1-indexed in solution and 0-indexed in input data
    print(team_data["mentors"][str(solution["team_assigned_mentor"][team_index] - 1)]) # mentors are 1-indexed in solution and 0-indexed in input data
    print(f"Percentage of the team present: {solution['team_score'][team_index]}")
    print()
    mentor_schedule_matrix[(solution["team_assigned_mentor"][team_index] - 1)].append(f"{time_index_to_date(team_time - 1)} with {team_data['teams'][str(team_index)]}")
print("=============================")
print()
print("## Mentors")
print(team_data["mentors"])
for k,v in enumerate(mentor_schedule_matrix):
    try:
        print()
        print("### ", team_data["mentors"][str(k)], " ###")
        for n in v:
            print(n)
    except:
        pass
