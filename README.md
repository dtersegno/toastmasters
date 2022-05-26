Toastmasters scheduler
---
```
python toastmasters.py (names_list_path = ./names.txt
                       (schedule_path = ./toastmasters_schedule.csv
                       (verbose = True
                       (random_seed = 20221
                       ))))
```

Creates a random schedule for a multi-day [Toastmasters](https://www.toastmasters.org/)-style conference given a list of names. Effectively a giant rectangular _Sudoku_ with misshapen and disconnected inner regions.

The Jupyter notebook is an initial scratchwork version of the code.

---
### arguments
- `names_list_path` a file with names to fill the schedule
- `schedule_path` a file to write a csv schedule. Will overwrite.
- `verbose` whether to print stuff
- `random_seed` determines the random placement. Many seeds result in an unusuable schedule. Use verbose to get a report. The default seed fills a 23-person conference without problems.

---
### the problem
Every day, the people are assigned a role. The roles come in several classes:
- Speaker roles (x3/day)
    - Prepared Speaker
    - Impromptu Speaker
    - Evaluator
- Leadership roles 
    - Toastmaster
    - President
    - Table Topics Master
    - General Evaluator
- Support roles
    - Greeter
    - Joke Master
    - Timer
    - Grammarian
    - Word of the Day
    - Ah Counter
    - Ballot Counter
    - Thought of the day
    - Sergeant at arms
    - Stand-in

All constraints:
- Every attendee must do each of the speaker roles once and only once during the conference.
- Everyone must do any of the leadership roles at least once.
- No attendee may have more than one role on a given day (an exception for "overflow" speakers ahead).
- Preferentially do not repeat a support role.
- Evaluators evaluate prepared speakers. It is preferable for a prepared speaker / evaluator pair to not be evaluator / prepared speaker later.
- Attendees who have been a Toastmaster, President, or Table Topics Master ought to not do any of those three jobs again. If they must be a leader again, they ought to be General Evaluator.
- If a day cannot be filled with 3 of each of the speaker roles at the end of the schedule, assign the leftover attendees as 4th speakers on earlier days.
    - Assign the 4th Impromptu Speakers on different days as the 4th Prepared Speakers / Evaluators.
- Ensure no attendee has more than one role each day.
    - Make an exception for 4th speakers. Preferentially assign 4th speakers where they are Stand-ins, or other support roles.
    
### procedure
`toastmasters.py` is a paint-into-a-corner search. It randomly fills a day's role assignments with available attendee names, checks if the day agrees with most of the constraints. If so, it commits and moves on to the next day. If not, it randomly fills the roles again. It gives up after 1000 attempts for each day. By the last day, most assignments have been given and there are not many valid schedules, and the likelihood of the search failing increases. If a search fails, try a different randomizer seed.
