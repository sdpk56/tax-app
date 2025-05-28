from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests

app = Flask(__name__)
app.secret_key = 'your-very-secure-secret-key'  # Replace with a strong, random secret key
BACKEND_URL = "http://backend-service:5000"  # Update this if your backend URL is different

@app.route('/')
def index():
    """Renders the homepage."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and password are required!', 'danger')
            return render_template('register.html')

        try:
            response = requests.post(
                f"{BACKEND_URL}/signup",
                json={"username": username, "password": password}
            )
            data = response.json()

            if response.status_code == 200:
                flash(data.get('message', 'Registration successful!'), 'success')
                return redirect(url_for('login'))
            else:
                flash(data.get('message', 'Registration failed. Please try again.'), 'danger')
        except requests.exceptions.ConnectionError:
            flash("Could not connect to the backend. Please check the backend server.", 'danger')
        except Exception as e:
            flash(f"An error occurred: {e}", 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and password are required!', 'danger')
            return render_template('login.html')

        try:
            response = requests.post(
                f"{BACKEND_URL}/login",
                json={"username": username, "password": password}
            )
            data = response.json()

            if response.status_code == 200 and 'access_token' in data:
                session['access_token'] = data['access_token']
                session['username'] = username  # Store username for display
                flash('Login successful!', 'success')
                return redirect(url_for('calculate_tax_form'))
            else:
                flash(data.get('message', 'Login failed. Please check your credentials.'), 'danger')
        except requests.exceptions.ConnectionError:
            flash("Could not connect to the backend. Please check the backend server.", 'danger')
        except Exception as e:
            flash(f"An error occurred: {e}", 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logs out the user by clearing the session."""
    session.pop('access_token', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/calculate-tax', methods=['GET', 'POST'])
def calculate_tax_form():
    """Displays the tax calculation form and handles tax calculation requests."""
    if 'access_token' not in session:
        flash('Please log in to calculate tax.', 'warning')
        return redirect(url_for('login'))

    tax_result = None
    if request.method == 'POST':
        income = request.form.get('income')
        regime = request.form.get('regime')

        if not income or not regime:
            flash('Income and tax regime are required!', 'danger')
            return render_template('calculate_tax.html', tax_result=tax_result)

        try:
            income = float(income)
        except ValueError:
            flash('Income must be a valid number.', 'danger')
            return render_template('calculate_tax.html', tax_result=tax_result)

        headers = {
            "Authorization": f"Bearer {session['access_token']}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                f"{BACKEND_URL}/calculate-tax",
                headers=headers,
                json={"income": income, "regime": regime}
            )
            data = response.json()

            if response.status_code == 200 and 'tax' in data:
                tax_result = data
                flash('Tax calculated successfully!', 'success')
            elif response.status_code == 401:
                flash(data.get('message', 'Unauthorized. Please log in again.'), 'danger')
                session.pop('access_token', None) # Clear invalid token
                return redirect(url_for('login'))
            else:
                flash(data.get('message', 'Tax calculation failed. Please try again.'), 'danger')
        except requests.exceptions.ConnectionError:
            flash("Could not connect to the backend. Please check the backend server.", 'danger')
        except Exception as e:
            flash(f"An error occurred: {e}", 'danger')

    return render_template('calculate_tax.html', tax_result=tax_result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000) # Run on port 8000 for frontend