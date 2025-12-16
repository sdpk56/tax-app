from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import requests
import os

# Minimal change for testing AI PR review

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-very-secure-secret-key')
BACKEND_URL = os.getenv('BACKEND_URL', 'http://tax-backend:5000')

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
                json={"username": username, "password": password},
                timeout=5
            )
            
            # Check if response has content
            if not response.text:
                flash("Backend server is not responding. Please check the backend service.", 'danger')
                return render_template('register.html')
            
            data = response.json()

            if response.status_code in [200, 201]:
                flash(data.get('message', 'Registration successful!'), 'success')
                return redirect(url_for('login'))
            elif response.status_code == 409:
                flash(data.get('message', 'Username already exists. Please try another.'), 'warning')
            else:
                flash(data.get('message', 'Registration failed. Please try again.'), 'danger')
        except requests.exceptions.Timeout:
            flash("Backend server is taking too long to respond. Please try again later.", 'danger')
        except requests.exceptions.ConnectionError:
            flash("Could not connect to the backend. Please check if the backend server is running.", 'danger')
        except ValueError as e:
            flash(f"Invalid response from backend: {str(e)}. Backend might be down.", 'danger')
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'danger')

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
                json={"username": username, "password": password},
                timeout=5
            )
            
            # Check if response has content
            if not response.text:
                flash("Backend server is not responding. Please check the backend service.", 'danger')
                return render_template('login.html')
            
            data = response.json()

            if response.status_code == 200 and 'access_token' in data:
                session['access_token'] = data['access_token']
                session['username'] = username  # Store username for display
                flash('Login successful!', 'success')
                return redirect(url_for('calculate_tax_form'))
            else:
                flash(data.get('message', 'Login failed. Please check your credentials.'), 'danger')
        except requests.exceptions.Timeout:
            flash("Backend server is taking too long to respond. Please try again later.", 'danger')
        except requests.exceptions.ConnectionError:
            flash("Could not connect to the backend. Please check if the backend server is running.", 'danger')
        except ValueError as e:
            flash(f"Invalid response from backend: {str(e)}. Backend might be down.", 'danger')
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'danger')

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

    return render_template('calculate_tax.html')


@app.route('/api/calculate-tax', methods=['POST'])
def api_calculate_tax():
    """API endpoint for tax calculation."""
    if 'access_token' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    headers = {"Authorization": f"Bearer {session['access_token']}"}

    try:
        response = requests.post(
            f"{BACKEND_URL}/calculate-tax",
            json=data,
            headers=headers
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"message": "Could not connect to backend"}), 503
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/api/compare-regimes', methods=['POST'])
def api_compare_regimes():
    """API endpoint for regime comparison."""
    if 'access_token' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    headers = {"Authorization": f"Bearer {session['access_token']}"}

    try:
        response = requests.post(
            f"{BACKEND_URL}/compare-regimes",
            json=data,
            headers=headers
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"message": "Could not connect to backend"}), 503
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/tax-history', methods=['GET'])
def view_tax_history():
    """Display user's tax calculation history."""
    if 'access_token' not in session:
        flash('Please log in to view tax history.', 'warning')
        return redirect(url_for('login'))

    return render_template('tax_history.html')


@app.route('/api/tax-history', methods=['GET'])
def api_tax_history():
    """API endpoint for tax history."""
    if 'access_token' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    headers = {"Authorization": f"Bearer {session['access_token']}"}

    try:
        response = requests.get(
            f"{BACKEND_URL}/tax-history?page={page}&per_page={per_page}",
            headers=headers
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"message": "Could not connect to backend"}), 503
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/api/tax-history/<int:calc_id>', methods=['DELETE'])
def api_delete_tax_calculation(calc_id):
    """API endpoint to delete tax calculation."""
    if 'access_token' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    headers = {"Authorization": f"Bearer {session['access_token']}"}

    try:
        response = requests.delete(
            f"{BACKEND_URL}/tax-history/{calc_id}",
            headers=headers
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"message": "Could not connect to backend"}), 503
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/api/tax-slabs/<regime>', methods=['GET'])
def api_tax_slabs(regime):
    """API endpoint for tax slab breakdown."""
    if 'access_token' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    income = request.args.get('income', type=float)
    headers = {"Authorization": f"Bearer {session['access_token']}"}

    try:
        response = requests.get(
            f"{BACKEND_URL}/tax-slabs/{regime}?income={income}",
            headers=headers
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"message": "Could not connect to backend"}), 503
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000) # Run on port 8000 for frontend