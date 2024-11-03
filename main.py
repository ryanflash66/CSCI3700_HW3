from flask import Flask, render_template
import util

app = Flask(__name__)

username='raywu1990'
password='test'
host='127.0.0.1'
port='5432'
database='dvdrental'

# Add a new route for updating basket_a
@app.route('/api/update_basket_a', methods=['GET'])
def update_basket_a():
    try:
        # Connect to the database
        cursor, connection = util.connect_to_db(username, password, host, port, database)

        # Insert a new row into basket_a
        insert_sql = "INSERT INTO basket_a (a, fruit_a) VALUES (5, 'Cherry');"
        result = util.run_and_commit_sql(cursor, connection, insert_sql)

        # Check if the operation was successful
        if result == 1:
            message = "Success!"
        else:
            message = "Error: Unable to insert the row"

    except Exception as e:
        # Return any exception that occurs
        message = f"Error: {str(e)}"

    finally:
        # Disconnect from the database
        if 'connection' in locals() and 'cursor' in locals():
            util.disconnect_from_db(connection, cursor)

    # Return the message in the browser
    return message


# Add a new route for showing unique fruits from basket_a and basket_b
@app.route('/api/unique', methods=["GET"])
def show_unique_fruits():
    try:
        # Connect to the database
        cursor, connection = util.connect_to_db(username, password, host, port, database)

        # Fetch unique fruits from basket_a and basket_b
        fruits_a = util.run_and_fetch_sql(cursor, "SELECT DISTINCT fruit_a FROM basket_a;")
        fruits_b = util.run_and_fetch_sql(cursor, "SELECT DISTINCT fruit_b FROM basket_b;")

        if fruits_a == -1 or fruits_b == -1:
            return "Error: Unable to fetch unique fruits"

        # Combine the results for rendering in HTML
        unique_fruits = {
            "Basket A": [fruit[0] for fruit in fruits_a],
            "Basket B": [fruit[0] for fruit in fruits_b]
        }

        # Render the HTML template with the unique fruits
        return render_template('unique_fruits.html', fruits=unique_fruits)

    except Exception as e:
        # Return any exception that occurs
        return str(e)

    finally:
        # Disconnect from the database
        if 'connection' in locals() and 'cursor' in locals():
            util.disconnect_from_db(connection, cursor)


if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(host='127.0.0.1', port=5000, debug=True)