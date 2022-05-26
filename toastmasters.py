####
# toastmasters.py name_list_path (output_file_path, (verbose, (random_seed)))
####

##############
#imports and arguments
##############
import sys

import numpy as np
import pandas as pd

#number of system passed arguments
numargs = len(sys.argv)
if numargs >= 2:
    student_name_path = './' + sys.argv[1]
else:
    student_name_path = './class_names.txt'
if numargs >= 3:
    output_file_path = './' + sys.argv[2]
else:
    output_file_path = './toastmasters_schedule.csv'
if numargs >=4 and sys.argv[3] == 'True':
    verbose = True
else:
    verbose = False
if numargs == 5:
    seed = int(sys.argv[4])
else:
    seed = 20221

###############
# name handling
###############
#get a list of the student names
name_list = pd.read_csv(student_name_path, header = None).values.flatten()
num_students = len(name_list)
# each day accounts for 3 repeat prepared speakers, impromptu speakers, and evaluators.
# overflows will be assigned as 4th speakers on 1 or 2 days.
num_days = num_students//3

#assign dummy names for scheduling
students = 'abcdefghijklmnopqrstuvwxyz'[:num_students]

#create a list of dummy names
full_student_list = [
        char for char in students
]

#create a dictionary to convert dummies to names later.
class_names_converter = {
    full_student_list[index]:name_list[index]
    for index in range(len(full_student_list))
}

###############
# roles
###############
# list collections of roles. these are combinations of roles by name, but also by placement (prepared speaker vs prepared speaker 1/2/3)

speaker_roles = ['Prepared Speaker',
                'Impromptu Speaker',
                'Evaluator'
]

prepared_speakers = ['Prepared Speaker 1',
                     'Prepared Speaker 2',
                     'Prepared Speaker 3'
]

evaluators = [
    'Evaluator 1',
    'Evaluator 2',
    'Evaluator 3'
]

impromptu_speakers = [
    'Impromptu Speaker 1',
    'Impromptu Speaker 2',
    'Impromptu Speaker 3'    
]

speakers = ['Prepared Speaker 1',
           'Impromptu Speaker 1',
           'Evaluator 1',
            'Prepared Speaker 2',
            'Impromptu Speaker 2',
            'Evaluator 2',
            'Prepared Speaker 3',
            'Impromptu Speaker 3',
            'Evaluator 3'
]

#removed general evaluator!
leaders = [
            'Toastmaster',
            'President',
            'Table Topics Master'
]

general_evaluators = [
    'General Evaluator'
]

auxiliary = ['Greeter',
            'Joke Master',
            'Timer',
            'Grammarian',
            'Word of the Day',
            'Ah Counter',
            'Ballot Counter',
            'Thought of the day',
            'Sergeant at arms',
            'Stand-in'
]


#####################
# checking functions
#####################
# these check if the calendar satisfies certain requirements
#everyone has to do each of the three types of speeches once and only once

# returns True if there are no repeat assignments for the given jobs.
# people can do multiple jobs, but not not the same job twice
def check_job_repeats(calendar, jobs = []):
    #check all columns if none given
    if len(jobs) == 0:
        jobs = calendar.columns
    result = True
    for job in jobs:
        if calendar[job].duplicated().sum() > 0:
            result = False
        #if any of the jobs have duplicates, finish the scan
        if not result:
            break
    return result


# nobody should have more than one job a day

# Checks if all the jobs on all the days of a dataframe are uniquely assigned --- no person has more than 1 job.
# returns True if so.
def check_day_repeats(calendar, days = []):
    if len(days) == 0:
        days = calendar.index
    result = True
    for row in days:
        if calendar.loc[row].duplicated().sum() > 0:
            result = False
        if not result:
            break
    return result

#returns true if there are no duplicates in the entire collection of job_list
def check_job_type_repeats(calendar, job_list, up_to_day):
    these_values = calendar.loc[:up_to_day, job_list].values.flatten()
    #print(these_values)
    try:
        u, c = np.unique(these_values, return_counts=True)
    except:
        print(f'Had a problem with these values:')
        print(these_values.reshape(-1,len(job_list)))
    dup = u[c > 1]
    return len(dup) == 0

#returns true if no prepared speaker /evaluator pairs occur more than once.
def check_speaker_evaluator_repeats(calendar):
    face_off_list = []
    speaker_evaluator_pairs = list(zip(prepared_speakers, evaluators))
    no_problems = True
    for day in calendar.index:
        for pair in speaker_evaluator_pairs:
            this_pair = set(calendar.loc[day, list(pair)])
            if this_pair in face_off_list:
                no_problems = False
            else:
                face_off_list.append(this_pair)
    return no_problems

###################
# filling functions
###################
# these fill calendar by roles accounting for which jobs need to be filled and which students are available

#fills in random roles for columns like prepared speaker 1,2,3.
def fill_repeated_roles(calendar, list_of_calendar_columns, role_dictionary, role_to_fill, day_dictionary, day):
    for role in list_of_calendar_columns:
                allowed_students = np.intersect1d(day_dictionary[day], role_dictionary[role_to_fill])
                #if the number of allowed students is less than 3, we've reached the end and only need to fill a few.
                #if that length is too short...
                if len(allowed_students) < 1:
                    #bail
                    return None
                else:
                    #pick out a student
                    this_student = rng.choice(allowed_students)
                    #remove the student from the day bucket
                    day_dictionary[day].remove(this_student)
                    #remove the student from the role bucket
                    role_dictionary[role_to_fill].remove(this_student)
                    #assign them that role
                    calendar.loc[day, role] = this_student
                    
#almost the same as above, but each role has its own entry in the role dictionary.
#Only changed roll_to_fill for role dictionary to role.
#this is used for the leadership roles
def fill_distinct_roles(calendar, list_of_calendar_columns, role_dictionary, day_dictionary, day):
    for role in list_of_calendar_columns:
                allowed_students = np.intersect1d(day_dictionary[day], role_dictionary[role])
                #if the number of allowed students is less than 3, we've reached the end and only need to fill a few.
                #if that length is too short...
                if len(allowed_students) < 1:
                    #bail
                    return None
                else:
                    #pick out a student
                    this_student = rng.choice(allowed_students)
                    #remove the student from the day bucket
                    day_dictionary[day].remove(this_student)
                    #remove the student from the role bucket
                    role_dictionary[role].remove(this_student)
                    #assign them that role
                    calendar.loc[day, role] = this_student

##########################
# preparation for search
##########################

# make an rng
rng = np.random.default_rng(seed)

# search settings.
# How many times to try filling a day
day_fill_counter_max = 1000


###############################
# fill a calendar with schedule
###############################

#create calendar as pandas DataFrame
cal = pd.DataFrame(columns = speakers + leaders + general_evaluators + auxiliary, index = range(num_days))
cal.index.rename('day', inplace=True)

#available students by day
student_buckets_by_day = {
    day:full_student_list.copy()
    for day in cal.index
}

#available students by role
student_buckets_by_role = {
    role:full_student_list.copy()
    for role in speaker_roles + ['Leaders'] + general_evaluators + auxiliary
}

#fill roles
for day in cal.index:
    if verbose:
        print(f'Filling speaker and leadership roles for day {day}.')
    #keep track whether we're done with the day at hand.
    day_filled = False
    #keep track of how many times we've attempted to fill the day. This is a random process and it's possible it won't work
    day_fill_counter = 0
    # keep track of original role buckets so they can be reset if it is misfilled
    this_day_original_role_buckets = student_buckets_by_role
    # until we're done 
    while not day_filled and day_fill_counter < day_fill_counter_max:
        day_fill_counter += 1
        #refill day's availability bucket. All students are available to be assigned roles from the day's POV.
        student_buckets_by_day[day] = list(full_student_list)
        #refill role buckets
        student_buckets_by_role = this_day_original_role_buckets
        #fill the prepared speaker roles
        fill_repeated_roles(cal, prepared_speakers, student_buckets_by_role, 'Prepared Speaker', student_buckets_by_day, day)
        #fill the impromptu speaker roles
        fill_repeated_roles(cal, impromptu_speakers, student_buckets_by_role, 'Impromptu Speaker', student_buckets_by_day, day)
        #fill the evaluator roles
        fill_repeated_roles(cal, evaluators, student_buckets_by_role, 'Evaluator', student_buckets_by_day, day)
        #fill the leadership roles
        fill_repeated_roles(cal, leaders, student_buckets_by_role, 'Leaders', student_buckets_by_day, day)
        #fill the general evaluators
        fill_distinct_roles(cal, general_evaluators, student_buckets_by_role, student_buckets_by_day, day)
        #fill the auxiliary roles
        fill_distinct_roles(cal, auxiliary, student_buckets_by_role, student_buckets_by_day, day)
        #check if there are no repeats in the day for the filled roles so far
        no_day_repeats = check_day_repeats(cal.loc[:day,speakers])
        #same for jobs
        no_job_repeats = check_job_repeats(cal.loc[:day,speakers])
        if no_day_repeats and no_job_repeats and cal.loc[day].isna().sum() == 0:
            day_filled = True
            if verbose:
                print(f'found a solution for day {day}.')
    if not day_filled and verbose:
        print(f'Failed to fill day {day} in {day_fill_counter_max} iterations.')

        
        
        
        

#attempt to fill in remaining speaker roles.
cal[['Prepared Speaker 4','Impromptu Speaker 4','Evaluator 4']] = np.nan
if verbose:
    print('Filling leftover students in 4th speaker roles.')
# replace any stand-ins left to impromptu-speak as that day's 4th impromptu speaker
for leftover_student in student_buckets_by_role['Impromptu Speaker']:
    for day in cal.index:
        if cal.loc[day, 'Stand-in'] == leftover_student:
            cal.loc[day, 'Impromptu Speaker 4'] = leftover_student
            student_buckets_by_role['Impromptu Speaker'].remove(leftover_student)
# replace any stand-ins left to prepared_speak as that day's 4th prepared speaker.
# look for days where the evaluator candidate is doing a support role.
for leftover_student in student_buckets_by_role['Prepared Speaker']:
    for day in cal.index:
        #check if any of the leftover evaluators are support roles
        support_eval_intersection = np.intersect1d(student_buckets_by_role['Evaluator'], cal.loc[day, auxiliary])
        if cal.loc[day, 'Stand-in'] == leftover_student and len(support_eval_intersection) > 0:
            cal.loc[day, 'Prepared Speaker 4'] = leftover_student
            student_buckets_by_role['Prepared Speaker'].remove(leftover_student)
            cal.loc[day, 'Evaluator 4'] = support_eval_intersection[0]
            student_buckets_by_role['Evaluator'].remove(support_eval_intersection[0])
    #if that didn't work, just look for days where both are in support roles.
for leftover_student in student_buckets_by_role['Prepared Speaker']:
    for day in cal.index:
        support_eval_intersection = np.intersect1d(student_buckets_by_role['Evaluator'], cal.loc[day, auxiliary])
        if (leftover_student in cal.loc[day, auxiliary].values) and (len(support_eval_intersection) > 0):
            #print(f'filling {leftover_student}, {support_eval_intersection[0]}')
            cal.loc[day, 'Prepared Speaker 4'] = leftover_student
            student_buckets_by_role['Prepared Speaker'].remove(leftover_student)
            cal.loc[day, 'Evaluator 4'] = support_eval_intersection[0]
            student_buckets_by_role['Evaluator'].remove(support_eval_intersection[0])
# attempt to fill any remaining impromptu speakers on days they are doing auxiliary roles.
for leftover_student in student_buckets_by_role['Impromptu Speaker'].copy():
    student_placed = False
    for day in cal.index:
        if (leftover_student in cal.loc[day, auxiliary].values) and cal.isna().loc[day,'Prepared Speaker 4'] and cal.isna().loc[day,'Impromptu Speaker 4'] and not student_placed:
            cal.loc[day, 'Impromptu Speaker 4'] = leftover_student
            student_buckets_by_role['Impromptu Speaker'].remove(leftover_student)
            student_placed = True
            
#run some checks
if verbose:
    if cal[speakers + leaders + general_evaluators + auxiliary].isna().sum().sum() > 0:
        print(f'There are some non-4th speaker assignments without a student.')
    for role in student_buckets_by_role:
        if role in speaker_roles and len(student_buckets_by_role[role]) > 0:
            print(f'There are unassigned {role} roles.')
    if not check_speaker_evaluator_repeats(cal):
        print(f'There are some repeat prepared speaker / evaluator pairs.')
    if len(student_buckets_by_role['Prepared Speaker']) > 0:
        print(f'There are students who have not been Prepared Speaker.')
    if len(student_buckets_by_role['Impromptu Speaker']) > 0:
        print(f'There are students who have not been Impromptu Speaker.')
    if len(student_buckets_by_role['Evaluator']) > 0:
        print(f'There are students who have not been Evaluator.')


################
# replace dummy names with real names and save the schedule
################
final_schedule = cal.replace(class_names_converter)
final_schedule.to_csv(output_file_path)