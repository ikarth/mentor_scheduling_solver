import os
import sys
import json
import pprint
import numpy
import random

#pprint.pprint(mentor_schedules)
print("""
=== Data Processor ===
Processes the schedule JSON (input filenames currently hard-coded below) and
transforms it into the JSON format the constraint solver needs. This was going
to be a lot harder before I realized the constraint solver could use JSON.


""")

print("Assumes that all names within a when2meet list sort in a stable order when upper-cased.")

def makePeopleSet(input_schedules, skip_extra_mentors=False, extra_mentors=[]):
    people = []
    for days in input_schedules:
        for hour in days:
            people.extend(hour)
    people_set = sorted(list(set(people)), key = str.upper)
    if skip_extra_mentors:
        #extra_mentor = "EXAMPLE EXTRA MENTOR WHO DOESN'T ACTUALLY EXIST"
        for extra_mentor in extra_mentors:
            try:
                people_set.remove(extra_mentor)
            except:
                pass
    print(people_set)
    print(len(people_set))
    print([[a,b] for a,b in enumerate(people_set)])
    return people_set

def makeScheduleMatrixRandom(input_schedules, team_people_set):
    """
    Makes a random schedule, mostly for testing purposes.
    """
    sch = numpy.ones([len(input_schedules) * len(input_schedules[0]), len(team_people_set)], dtype=bool)
    rnd = numpy.random.random_sample([len(input_schedules) * len(input_schedules[0]), len(team_people_set)])
    sch = rnd > 0.39
    return sch


def makeScheduleMatrix(input_schedules, team_people_set):
    """
    Translates the input schedule format (with a list of names in each
    scheduling slot, representing who is available in that slot) into an array
    with the count of how many people are available for each slot.
    """
    number_of_days = len(input_schedules)
    number_of_hours = len(input_schedules[0])
    sch = numpy.zeros([len(team_people_set), number_of_days * number_of_hours], dtype=bool)
    for day_num, day in enumerate(input_schedules):
        for hour_num, hour in enumerate(day):
            for count, person in enumerate(team_people_set):
                if person in hour:
                    sch[count, (day_num * number_of_hours) + hour_num] = True
    print(sch.shape)
    return sch

def compareMentorsAndTeams(mentor_sch, team_sch):
    """
    Teams can only meet with the mentors when the mentors are available, so
    for each mentor multiply the 0..1 mentor value against the team team
    availability count to use the mentor schedule as a mask over the team
    schedule.

    We could rewrite the constraint solver model to do this processing step,
    but we might as well save the time and do it as part of the pre-processing.
    """
    team_max = numpy.amax(team_sch.sum(axis=0))
    team_availability_score = 100 * (team_sch.sum(axis=0) / team_max)
    compare_sch = numpy.zeros(mentor_sch.shape, dtype=numpy.int16)
    for m in range(compare_sch.shape[0]):
        compare_sch[m] = team_availability_score * mentor_sch[m]
    return compare_sch


def write_datafile_as_json(mentor_schedules, team_availability_schedule, team_data, mentor_list):
    """
    Export to the JSON that the constraint solver model understands.

    Also export the names and stuff so that the solution interperter can
    use them when reporting on the results, because the solver only cares
    about the numbers and it's best if it stays that way.
    """
    split_team_data = {"teams": {k:v.replace("calendar_","").replace(".json", "") for k,v in enumerate(team_data)} }
    split_team_data["mentors"] = {k:v for k,v in enumerate(mentor_list)}
    with open("split_01_teams.json", "w") as dzn_json:
        json.dump(split_team_data, dzn_json)
    data = {}
    data["number_of_mentors"] = mentor_schedules.shape[0]
    data["number_of_teams"] = len(team_availability_schedule)
    data["number_of_slots"] = mentor_schedules.shape[1]
    print(f"number of mentors: {mentor_schedules.shape[0]}")
    print(f"number of teams: {len(team_availability_schedule)}")
    print(f"number of slots: {mentor_schedules.shape[1]}")
    teams_per_mentor = numpy.zeros([team_availability_schedule[0].shape[0], len(team_availability_schedule), team_availability_schedule[0].shape[1]], dtype=numpy.int16)
    for m in range(team_availability_schedule[0].shape[0]):
        for t in range(len(team_availability_schedule)):
            for s in range(team_availability_schedule[0].shape[1]):
                avail = team_availability_schedule[t][m,s]
                teams_per_mentor[m,t,s] = avail
    print(teams_per_mentor.shape)
    print(teams_per_mentor.shape[0] * teams_per_mentor.shape[1] * teams_per_mentor.shape[2])
    data["team_availability_per_mentor"] = teams_per_mentor.tolist()
    with open("split_01_data.json", "w") as dzn_json:
        json.dump(data, dzn_json)

def load_team_data(team_filename):
    schedules = []
    with open(team_filename, "r") as f:
        schedules = json.load(f)
    people_set = makePeopleSet(schedules)
    return [makeScheduleMatrix(schedules, people_set), people_set]


mentor_schedules = []
with open("mentor_calendar.json", "r") as f:
    mentor_schedules = json.load(f)
mentor_set = makePeopleSet(mentor_schedules, skip_extra_mentors=False)
#mentor_set.extend(["Alice", "Bob"])#, "Eve", "Harold"])
mentor_sch_matrix = makeScheduleMatrix(mentor_schedules, mentor_set)

tad_schedules = []
with open("calendar_tad_split_01.json", "r") as f:
    tad_schedules = json.load(f)
tad_set = makePeopleSet(tad_schedules)
tad_sch_matrix = makeScheduleMatrix(tad_schedules, tad_set)

# These, of course, should be changed to match the current team schedules.
# The format is nested JSON arrays:
# - schedules
#   - days
#     - time slots (15 minutes)
#       - names of the people available at that time (from when2meet)
# Note that while the when2meet data is in 15-minute slots, the solver model
# by default only look at the ones that start on the hour or half-hour because
# we're trying to schedule 30-minute meetings
team_data_files = [
    "calendar_team_001.json",
    "calendar_team_002.json",
    "calendar_team_003.json",
    "calendar_team_004.json",
    "calendar_team_005.json",
    "calendar_team_006.json",
    "calendar_team_007.json",
    "calendar_team_008.json",
    "calendar_team_010.json",
    "calendar_team_011.json",
    "calendar_team_012.json",
    "calendar_team_013.json",
    "calendar_team_014.json",
    "calendar_team_015.json",
    "calendar_team_016.json",
    "calendar_team_017.json",
    "calendar_team_018.json",
    "calendar_team_019.json",
    "calendar_team_020.json",
    "calendar_team_021.json",
    "calendar_team_022.json",
    "calendar_team_023.json",
    "calendar_team_024.json",
    "calendar_team_025.json"]
team_schedules = [load_team_data(x) for x in team_data_files]

print( [f"{k}:{v.replace('calendar_','').replace('.json', '')}" for k,v in enumerate(team_data_files)] )

for n in range(len(team_schedules[19][0])):
    team_schedules[19][0][n] = team_schedules[19][0][n] * tad_sch_matrix[0]
team_availability = [compareMentorsAndTeams(mentor_sch_matrix, x[0]) for x in team_schedules]

write_datafile_as_json(mentor_sch_matrix, team_availability, team_data_files, mentor_set)
