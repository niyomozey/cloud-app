from flask import Flask, request, render_template, redirect, url_for
from cassandra_config import CassandraConnector

# Create a Flask app
app = Flask(__name__)
cassandra_connector = CassandraConnector()
data_buffer = []

# Define a route for the home page
@app.route("/")
def home():
    # Render a template that asks for user input
    return render_template("app.html")

# Define a route for the result page
@app.route("/result", methods=["GET","POST"])
def result():
    # Get the user input from the form
    name = request.form.get("name")
    andrewID = request.form.get("andrewID")
    course = request.form.get("course")
    grade = request.form.get("grade")
    try:
        cassandra_connector.save_data(name, andrewID, course, grade)
    except Exception as e:
        print(f"Failed to save data to Cassandra. Reason: {str(e)}")
        data_buffer.append({'name': name, 'andrewid': andrewID, 'course': course, 'grade': grade})

    return redirect(url_for('display'))

    # Render a template that shows the result
    # return render_template("result.html")
    return redirect(url_for('display'))

@app.route('/display')
def display():
    data = cassandra_connector.get_all_data() + data_buffer
    return render_template('display.html', data=data)

# Run the app in debug mode
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
