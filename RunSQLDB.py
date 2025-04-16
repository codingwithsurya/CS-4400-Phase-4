
#!/usr/bin/env python3

from subprocess import Popen, PIPE
from io import StringIO
import pandas as pd
import webbrowser
import os

# Database 
db = 'flight_tracking'
user = 'root'

# MySQL files
sql_files = [
    'cs4400_sams_phase3_database_v0.sql',
    'cs4400_phase3_stored_procedures_team121.sql',
    'cs4400_sams_phase3_autograder_BASIC_v0.sql',
]

for i in sql_files:
    cmd = f'mysql -u {user} {db} < {i}'    
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    print(f"Executing SQL Script: {i}")
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())

scoring_summary = Popen([ 'mysql', '-u', f'{user}', '-e', 
                       "SELECT * FROM flight_tracking.magic44_autograding_score_summary;"]
                        , stdout=PIPE, stderr=PIPE)

## Traceable errors
traceable_errors = Popen([ 'mysql', '-u', f'{user}', '-e', 
                       "SELECT * FROM flight_tracking.magic44_column_errors_traceable;"]
                        , stdout=PIPE, stderr=PIPE)
## Errors Stored Procedures
stored_procedures = Popen([ 'mysql', '-u', f'{user}', '-e', 
                       "SELECT * FROM flight_tracking.magic44_column_errors;"]
                        , stdout=PIPE, stderr=PIPE)

stdout, stderr = scoring_summary.communicate()

stdout_trac, stderr_trac = traceable_errors.communicate()

## Load Stored Procedure Error Keys
stdout_sp, stderr_sp = stored_procedures.communicate()

data = [
    (10, 'airline'),
    (11, 'location'),
    (12, 'airplane'),
    (13, 'airport'),
    (14, 'person'),
    (15, 'passenger'),
    (16, 'passenger_vacations'),
    (17, 'leg'),
    (18, 'route'),
    (19, 'route_path'),
    (20, 'flight'),
    (21, 'pilot'),
    (22, 'pilot_licenses'),
    (30, 'flights_in_the_air'),
    (31, 'flights_on_the_ground'),
    (32, 'people_in_the_air'),
    (33, 'people_on_the_ground'),
    (34, 'route_summary'),
    (35, 'alternative_airports')
]

df_keys_sp = pd.DataFrame(data, columns=['query_id', 'Category'])


decoded_output = stdout.decode()
decode_errors=stdout_trac.decode()
decode_errors_sp=stdout_sp.decode()


data = StringIO(decoded_output)
data_errors = StringIO(decode_errors)
data_errors_sp = StringIO(decode_errors_sp)

df = pd.read_csv(data, sep='\t')
try:
    df_errors = pd.read_csv(data_errors, sep='\t')
except:
    pass
## Join with keys
try:
    df_errors_sp = pd.read_csv(data_errors_sp, sep='\t')
except:
    pass
try:
    df_errrors_sp_join = pd.merge(df_errors_sp, df_keys_sp, on='query_id')
except:
    pass



# Apply a border to table
styled_df = df.style.set_table_attributes('style="border-collapse: collapse; border: 1px solid black;"')
try:
    styled_df_errors = df_errors.style.set_table_attributes('style="border-collapse: collapse; border: 1px solid black;"')
except:
    pass
try:
    df_errrors_sp_join = df_errrors_sp_join.style.set_table_attributes('style="border-collapse: collapse; border: 1px solid black;"')
except:
    pass

## DF
styled_df.to_html()
try:
    styled_df_errors.to_html()
except:
    pass
try:
    df_errrors_sp_join.to_html()
except:
    pass

## HTML Table
html_table = styled_df.to_html(border=1, index=False)
try:
    html_table_errors = styled_df_errors.to_html(border=1, index=False)
except:
    pass
try:
    html_table_error_sp = df_errrors_sp_join.to_html(border=1, index=False)
except:
    pass
# Save the HTML to a file
html_file = 'scoring_summary.html'
html_file_error = 'View_summary.html'
html_file_error_sp = 'SP_Summary.html'

with open(html_file, 'w') as f:
    f.write(html_table)
with open(html_file_error, 'w') as f:
    try:
        f.write(html_table_errors)
    except:
        pass
with open(html_file_error_sp, 'w') as f:
    try:
        f.write(html_table_error_sp)
    except:
        pass
file_path = os.path.abspath(html_file)
file_path_errors = os.path.abspath(html_file_error)
file_path_errors_sp = os.path.abspath(html_file_error_sp)

webbrowser.open(f'file://{file_path}')
try:
    html_table_error_sp = df_errrors_sp_join.to_html(border=1, index=False)
    webbrowser.open(f'file://{file_path_errors}')
    webbrowser.open(f'file://{file_path_errors_sp}')
except:
    pass

location_query = Popen(['mysql', '-u', f'{user}', '-e', 
                       "SELECT @@datadir;"], 
                      stdout=PIPE, stderr=PIPE)
stdout, stderr = location_query.communicate()
print("MySQL data directory:", stdout.decode())