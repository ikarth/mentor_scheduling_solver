include "globals.mzn";

int: number_of_mentors;
int: number_of_teams;
int: number_of_slots;
int: max_team_members = 100; % in percent


set of int: MENTORS = 1..number_of_mentors;
set of int: TEAMS = 1..number_of_teams;
set of int: TEAMS_PLUS_NIL = 0..number_of_teams;
set of int: SLOTS = 1..number_of_slots;
set of int: SLOTS_PLUS_NIL = 0..number_of_slots;
set of int: MAX_MEMBERS = 0..max_team_members;
set of int: MAX_INDEX = 0..((number_of_slots+1) * (number_of_mentors+1));

%array[SLOTS, TEAMS] of var MAX_MEMBERS: team_time;
array[MENTORS, TEAMS, SLOTS] of var MAX_MEMBERS: team_availability_per_mentor;
array[MENTORS, SLOTS] of var TEAMS_PLUS_NIL: a_mentor_assigned_teams_in_slots;

array[MENTORS, TEAMS_PLUS_NIL] of var SLOTS_PLUS_NIL: mentor_meeting_times;
array[TEAMS] of var SLOTS: team_assigned_meeting_times;
array[TEAMS] of var MENTORS: team_assigned_mentor;
array[TEAMS] of var MAX_INDEX: team_assigned_index;

array[MENTORS] of var TEAMS_PLUS_NIL: mentor_meeting_count;
array[MENTORS] of var 0..1000: mentor_score;
array[TEAMS] of var 0..100: team_score;
var 0..600: max_possible_score;
var 0..600: overall_score;


% Team can meet with mentor at specified time
constraint forall(i in TEAMS)(team_availability_per_mentor[team_assigned_mentor[i], i, team_assigned_meeting_times[i]] > 0);
% Team score is how many people can meet at that time
constraint forall(i in TEAMS)(team_score[i] = team_availability_per_mentor[team_assigned_mentor[i], i, team_assigned_meeting_times[i]]);

% Meetings are half an hour long, not 15 minutes
%constraint forall(i in TEAMS)(a_mentor_assigned_teams_in_slots[team_assigned_mentor[i], team_assigned_meeting_times[i] + 1, ] = 0);
% Meetings take place on the hour or half-hour
constraint forall(i in TEAMS)((team_assigned_meeting_times[i] mod 2) = 1);

% Mentor can only meet with one team per time slot
constraint forall(i in TEAMS)(mentor_meeting_times[team_assigned_mentor[i], i] = team_assigned_meeting_times[i]);
% Mentor can only meet with each team once (also implied by team_assigned_mentor, so redundant?)
constraint forall(i in MENTORS)(alldifferent_except_0(mentor_meeting_times[i,TEAMS_PLUS_NIL]));
% minimize the number of meetings each mentor has
constraint forall(i in MENTORS)(mentor_meeting_count[i] = nvalue(mentor_meeting_times[i,TEAMS_PLUS_NIL]));
constraint forall(i in MENTORS)(mentor_score[i] = 2 * (100 - (100 * (mentor_meeting_count[i] - 1)) div 10));

% only one meeting per team
constraint forall(j in TEAMS)(a_mentor_assigned_teams_in_slots[team_assigned_mentor[j], team_assigned_meeting_times[j]] = j);
constraint alldifferent_except_0(a_mentor_assigned_teams_in_slots);

constraint forall(j in TEAMS)(team_assigned_index[j] = team_assigned_meeting_times[j] + (team_assigned_mentor[j] * number_of_slots));
constraint alldifferent_except_0(team_assigned_index);

constraint overall_score = (sum(team_score) div number_of_teams) + (min(team_score) * 3) + min(mentor_score);

constraint max_possible_score = (100 + 300 + 120);
constraint overall_score <= max_possible_score;

% search annotations:
% variable choice:
% input_order, first_fail, anti_first_fail, smallest, largest, occurrence, most_constrained, max_regret, dom_w_deg
% assignment:
% indomain_min, indomain_max, indomain_middle, indomain_median, indomain, indomain_random, indomain_split, indomain_reverse_split, indomain_interval

solve :: int_search(team_assigned_index, largest, indomain_random)
  maximize overall_score;
