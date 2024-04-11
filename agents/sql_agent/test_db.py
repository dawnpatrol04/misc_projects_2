import sqlite3

def fetch_table_contents(db_path, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Construct the SQL query to fetch all data from the specified table
    query = f"SELECT * FROM {table_name}"
    
    try:
        # Execute the query
        cursor.execute(query)
        
        # Fetch all rows from the table
        rows = cursor.fetchall()
        
        # Fetch the column names
        columns = [description[0] for description in cursor.description]
        
        # Print the column names
        print(" | ".join(columns))
        
        # Print each row
        for row in rows:
            print(" | ".join(str(value) for value in row))
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the connection to the database
        conn.close()

# Usage example
db_path = '/Users/mikeparsons/Documents/code/misc_projects_2/agents/sql_agent/5G_Data_Sample.sqlite'  # Update this with the path to your SQLite database file
table_name = 'CELLTOWERDATA'  # Replace 'YourTableName' with the actual name of your table

# Call the function with your database path and table name
fetch_table_contents(db_path, table_name)
