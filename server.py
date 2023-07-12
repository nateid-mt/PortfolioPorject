# pylint: disable-all
import psycopg2
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

# Create a Flask web server
app = Flask(__name__)

# Configure the PostgreSQL connection
connection = psycopg2.connect(
    host="localhost",
    port="5433",
    database="news_app",
    user="username",
    password="password"
)

# Define the execute_sql_file function
def execute_sql_file(user):
    with open(user, 'r') as file:
        sql = file.read()
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        cursor.close()


# Execute the SQL file to create the database schema and tables
execute_sql_file('user.sql')


# Define an API endpoint to handle the preference data
@app.route('/preferences', methods=['POST'])
def save_preferences():
    """['Preferences saved successfully!', 'An error occurred while saving preferences.']"""
    # Retrieve the preference data from the request
    data = request.get_json()
    user_id = data.get('user_id')
    preferences = data.get('preferences')

    try:
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Insert the preference data into the 'data' table
        cursor.execute("INSERT INTO data (user_id, preferences) VALUES (%s, %s)", (user_id, preferences))

        # Commit the changes to the database
        connection.commit()

        # Close the cursor
        cursor.close()

        return "Preferences saved successfully!"
    except psycopg2.Error as error:
        print("Error saving preferences:", error)
        return "An error occurred while saving preferences."
    
def save_accounts():
    """Account saved successfully!', 'An error occurred while saving the account."""
    #Retrieve the account data from the reuest
    data = request.get_json()
    user_name = data.get('user_name')
    email = data.get('email')
    name = data.get('name')

    try:
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Insert the account data into the 'user' table
        cursor.execute("INSERT INTO \"user\" (user_name, email, name) VALUES (%s, %s, %s)", (user_name, email, name))

        # Commit the changes to the database
        connection.commit()

        # Close the cursor
        cursor.close()

        return "Account saved successfully!"
    except psycopg2.Error as error:
        print("Error saving account:", error)
        return "An error occurred while saving the account."
    
# Define an API endpoint to retrieve the preferences for a specific user
@app.route('/preferences/<int:user_id>', methods=['GET'])
def get_preferences(user_id):
    """Preferences not found for the given user ID.', 'An error occurred while retrieving preferences."""
    
    try:
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Retrieve the preferences for the given user ID from the 'data' table
        cursor.execute("SELECT preferences FROM data WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()

        # Close the cursor
        cursor.close()

        if result:
            preferences = result[0]
            return jsonify(preferences)
        else:
            return "Preferences not found for the given user ID."
    except psycopg2.Error as error:
        print("Error retrieving preferences:", error)
        return "An error occurred while retrieving preferences."

# Run the Flask web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)