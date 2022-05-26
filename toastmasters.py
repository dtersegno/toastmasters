####
# toastmasters.py name_list_csv 
# 



import sys

import numpy as np
import pandas as pd



 
num_students = sys.argv[1] #23


students = 'abcdefghijklmnopqrstuvwxyz'[:num_students]

full_student_list = [
        char for char in students
]

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

leaders = [
            'Toastmaster',
            'President',
            'Table Topics Master',
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