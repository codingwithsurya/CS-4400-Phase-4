from django.db import connection
import pymysql

def safe_execute_view_query(view_name):
    """
    Safely execute a query on a database view without Django's type conversion
    """
    # Connect directly to the database to avoid Django's typecasting
    db_settings = connection.settings_dict
    conn = pymysql.connect(
        host=db_settings['HOST'],
        user=db_settings['USER'],
        password=db_settings['PASSWORD'],
        database=db_settings['NAME'],
        port=db_settings['PORT'] or 3306,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {view_name}")
            results = cursor.fetchall()
            
            # Get column names
            columns = list(results[0].keys()) if results else []
            
            # Convert dict results to list of values
            row_values = []
            for row in results:
                row_values.append(list(row.values()))
                
            return columns, row_values
    finally:
        conn.close()
