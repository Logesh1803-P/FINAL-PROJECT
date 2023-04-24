from flask import Flask, render_template, request
import mysql.connector
import re

# Create a Flask app and define the database connection:
# python
# Copy code
app = Flask(__name__)

db = mysql.connector.connect(
    # host="localhost",
    # user="root",
    # password="",
    # database="xss_attacks"
     host="localhost",
     user="root",
     password="1803",
     database="xss_attacks"
)
# Create a function to check for different types of XSS attacks:
# python
# Copy code
# def detect_xss(input_str):
#     # Reflected XSS
#     input_str = html.escape(input_str)
#     if re.findall(r'script', input_str):
#         return 'Reflected XSS'
    
#     # Stored XSS
#     cursor = db.cursor()
#     query = "INSERT INTO xss_attacks (input) VALUES (%s)"
#     cursor.execute(query, (input_str,))
#     db.commit()
    
#     # DOM-based XSS
#     if re.findall(r'document', input_str):
#         return 'DOM-based XSS'
    
#     return None
# Reflected XSS detection pattern
reflected_xss_pattern = re.compile(r'<script>|<\/script>|<img|<svg|alert\(|confirm\(|prompt\(|javascript:', re.IGNORECASE)

# DOM-based XSS detection pattern
dom_xss_pattern = re.compile(r'document\.|window\.|eval\(|\$\(|\$\$|\$\$\$|\(\)\.innerHTML|location\.href', re.IGNORECASE)

def detect_xss(payload):
    # if reflected_xss_pattern.search(payload):
    #     print("Reflected XSS attack detected!")
    if dom_xss_pattern.search(payload):
        # print("DOM-based XSS attack detected!")
        return "DOM-based XSS attack detected!"
    elif reflected_xss_pattern.search(payload):
        # print("Reflected XSS attack detected!")
        return "Reflected XSS attack detected!"
    else:
        # print("No XSS attack detected.")
        return "No XSS attack detected."
# Create a route to handle the form submission:
# python
# Copy code
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check for XSS attacks
        xss_attack_username = detect_xss(username)
        xss_attack_password = detect_xss(password)
        
        # Store the results in the database
        cursor = db.cursor()
        query = "INSERT INTO users (username, password, xss_attack_username, xss_attack_password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, password, xss_attack_username, xss_attack_password))
        db.commit()
        
        # return 'Submitted successfully!'
        return render_template('image.html', image_url=username)
    
    return render_template('index.html')
# Create an HTML template for the form:
# html
# Copy code

# Run the Flask app:
# python
# Copy code

if __name__ == "__main__":
	app.run(debug=True)