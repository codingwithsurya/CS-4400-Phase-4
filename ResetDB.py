#!/usr/bin/env python3

from subprocess import Popen, PIPE
from io import StringIO
import subprocess
import pandas as pd
import webbrowser
import os

# Database 
db = 'flight_tracking'
user = 'root'
env = os.environ.copy()
env['MYSQL_PWD'] = 'suryavarshini123'

# MySQL files
sql_files = [
    'cs4400_sams_phase3_database_v0.sql',
    'cs4400_phase3_stored_procedures_team121.sql',
    'cs4400_sams_phase3_autograder_BASIC_v0.sql',
]

for i in sql_files:
    test=subprocess.run([f'mysql -u root flight_tracking < {i}'], env=env, shell=True, capture_output=True)
    print(f"Running {i}")