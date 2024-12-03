from flask import Flask, request, render_template_string

app = Flask(__name__)

EMAIL_FILE = "emails.txt"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Submission</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f7fa;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            width: 90%;
            max-width: 500px;
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        h1 {
            color: #333333;
            margin-bottom: 20px;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-bottom: 20px;
        }
        input[type="email"] {
            padding: 12px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 5px;
            transition: border-color 0.3s ease;
        }
        input[type="email"]:focus {
            border-color: #007BFF;
            outline: none;
        }
        input[type="submit"] {
            padding: 12px;
            font-size: 16px;
            background: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        input[type="submit"]:hover {
            background: #0056b3;
        }
        .message {
            margin-top: 10px;
            padding: 10px;
            background-color: #d4edda;
            color: #155724;
            border-radius: 5px;
            text-align: center;
        }
        .error {
            margin-top: 10px;
            padding: 10px;
            background-color: #f8d7da;
            color: #721c24;
            border-radius: 5px;
            text-align: center;
        }
        h2 {
            color: #333333;
            margin-top: 20px;
        }
        ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }
        li {
            padding: 10px;
            background-color: #f8f9fa;
            margin: 5px 0;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Email Submission</h1>
        <form method="POST" action="/">
            <input type="email" name="email" placeholder="Enter your email" required>
            <input type="submit" value="Submit">
        </form>
        {% if message %}
            <div class="message">{{ message }}</div>
        {% endif %}
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <h2>Submitted Emails</h2>
        <ul>
            {% for email in emails %}
                <li>{{ email }}</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

def read_emails():
    try:
        with open(EMAIL_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

def save_email(email):
    with open(EMAIL_FILE, "a") as file:
        file.write(email + "\n")

@app.route("/", methods=["GET", "POST"])
def home():
    emails = read_emails()
    message = None
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        if not email or "@" not in email:
            error = "Invalid email address."
        else:
            save_email(email)
            message = f"Email '{email}' stored successfully!"
            emails.append(email)
    return render_template_string(HTML_TEMPLATE, emails=emails, message=message, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
