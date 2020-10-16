# Mentor Scheduling Solver
Constraint solving model for scheduling UCSC CMPM 170 team/mentor meetings

Uses [MiniZinc](https://www.minizinc.org/) to generate schedules for the teams to meet with their mentors with schedules that work for everybody involved.

Basic usage:
* Download the when2meet data (using something like the code in data_extractor.js).
* Convert the data into the JSON format the MiniZinc model can read (data_processor.py, requires Numpy).
* Run the constraint model (schedule_teams.mzn; easiest way is using the MiniZinc IDE until an end-to-end control script is written).
* Take the solution the constraint solver finds, save it as JSON.
* Run the solution interperter to turn the arrays of numbers into something more readable (interpert_solutions.py).
