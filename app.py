from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Simulated user database
users = {}

def generate_recommendation(user_data):
    age = user_data['age']
    income = user_data['income']
    savings = user_data['savings']
    risk_tolerance = user_data['risk_tolerance']
    short_term_goal = user_data['short_term_goal']
    long_term_goal = user_data['long_term_goal']

    recommendation = {
        'stocks': 0,
        'mutual_funds': 0,
        'fd': 0,
        'gold': 0,
        'crypto': 0,
        'ppf': 0,
        'nps': 0,
        'scss': 0,
        'policies': 0
    }

    # Basic allocation based on risk tolerance
    if risk_tolerance == 'low':
        recommendation['fd'] = 30
        recommendation['ppf'] = 20
        recommendation['gold'] = 10
        recommendation['mutual_funds'] = 20
        recommendation['stocks'] = 10
        recommendation['nps'] = 10
    elif risk_tolerance == 'medium':
        recommendation['stocks'] = 30
        recommendation['mutual_funds'] = 30
        recommendation['fd'] = 15
        recommendation['ppf'] = 10
        recommendation['gold'] = 5
        recommendation['crypto'] = 5
        recommendation['nps'] = 5
    else:  # high risk tolerance
        recommendation['stocks'] = 40
        recommendation['mutual_funds'] = 25
        recommendation['crypto'] = 15
        recommendation['gold'] = 5
        recommendation['fd'] = 5
        recommendation['ppf'] = 5
        recommendation['nps'] = 5

    # Age-specific adjustments
    if age > 50:
        recommendation['scss'] = 10
        recommendation['stocks'] = max(0, recommendation['stocks'] - 10)
    elif 30 <= age <= 40:
        recommendation['ppf'] += 5
        recommendation['mutual_funds'] = max(0, recommendation['mutual_funds'] - 5)

    # Goal-specific adjustments
    if short_term_goal == 'emergency_fund':
        recommendation['fd'] += 10
        recommendation['stocks'] = max(0, recommendation['stocks'] - 10)
    elif short_term_goal == 'vacation':
        recommendation['mutual_funds'] += 5
        recommendation['fd'] += 5
        recommendation['stocks'] = max(0, recommendation['stocks'] - 10)

    if long_term_goal == 'retirement':
        recommendation['nps'] += 10
        recommendation['mutual_funds'] = max(0, recommendation['mutual_funds'] - 10)
    elif long_term_goal == 'children_education':
        recommendation['ppf'] += 10
        recommendation['mutual_funds'] += 5
        recommendation['stocks'] = max(0, recommendation['stocks'] - 15)

    # Ensure policies are included
    recommendation['policies'] = 5
    recommendation['stocks'] = max(0, recommendation['stocks'] - 5)

    return recommendation

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_data = {
        'age': int(request.form['age']),
        'income': int(request.form['income']),
        'savings': int(request.form['savings']),
        'risk_tolerance': request.form['risk_tolerance'],
        'short_term_goal': request.form['short_term_goal'],
        'long_term_goal': request.form['long_term_goal']
    }
    
    recommendation = generate_recommendation(user_data)
    
    user_id = len(users) + 1
    users[user_id] = {
        'data': user_data,
        'recommendation': recommendation,
        'created_at': datetime.now()
    }
    
    return jsonify({'user_id': user_id, 'recommendation': recommendation})

@app.route('/adjust', methods=['POST'])
def adjust():
    user_id = int(request.form['user_id'])
    field = request.form['field']
    value = request.form['value']
    
    if user_id in users:
        users[user_id]['data'][field] = value
        new_recommendation = generate_recommendation(users[user_id]['data'])
        users[user_id]['recommendation'] = new_recommendation
        return jsonify({'success': True, 'recommendation': new_recommendation})
    else:
        return jsonify({'success': False, 'error': 'User not found'})

@app.route('/track_progress', methods=['POST'])
def track_progress():
    user_id = int(request.form['user_id'])
    goal = request.form['goal']
    progress = float(request.form['progress'])
    
    if user_id in users:
        if 'progress' not in users[user_id]:
            users[user_id]['progress'] = {}
        users[user_id]['progress'][goal] = progress
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'User not found'})

if __name__ == '__main__':
    app.run(debug=True)

# HTML template (index.html) - place this in a 'templates' folder
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Financial Advisor</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: auto; }
        form { margin-bottom: 20px; }
        label { display: block; margin-top: 10px; }
        input, select { width: 100%; padding: 8px; margin-top: 5px; }
        button { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; margin-top: 10px; }
        #recommendation, #progressTracker { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Financial Advisor</h1>
        <form id="financialForm">
            <label for="age">Age:</label>
            <input type="number" id="age" name="age" required>
            
            <label for="income">Annual Income:</label>
            <input type="number" id="income" name="income" required>
            
            <label for="savings">Current Savings:</label>
            <input type="number" id="savings" name="savings" required>
            
            <label for="risk_tolerance">Risk Tolerance:</label>
            <select id="risk_tolerance" name="risk_tolerance" required>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
            </select>
            
            <label for="short_term_goal">Short-term Goal:</label>
            <select id="short_term_goal" name="short_term_goal" required>
                <option value="emergency_fund">Build Emergency Fund</option>
                <option value="vacation">Save for Vacation</option>
                <option value="new_car">Buy a New Car</option>
            </select>
            
            <label for="long_term_goal">Long-term Goal:</label>
            <select id="long_term_goal" name="long_term_goal" required>
                <option value="retirement">Retirement</option>
                <option value="buy_house">Buy a House</option>
                <option value="children_education">Children's Education</option>
            </select>
            
            <button type="submit">Get Recommendation</button>
        </form>
        
        <div id="recommendation" style="display: none;">
            <h2>Your Personalized Investment Recommendation</h2>
            <canvas id="recommendationChart"></canvas>
        </div>
        
        <div id="adjustments" style="display: none;">
            <h2>Adjust Your Information</h2>
            <form id="adjustForm">
                <label for="adjust_field">Field to Adjust:</label>
                <select id="adjust_field" name="adjust_field" required>
                    <option value="age">Age</option>
                    <option value="income">Income</option>
                    <option value="savings">Savings</option>
                    <option value="risk_tolerance">Risk Tolerance</option>
                    <option value="short_term_goal">Short-term Goal</option>
                    <option value="long_term_goal">Long-term Goal</option>
                </select>
                
                <label for="adjust_value">New Value:</label>
                <input type="text" id="adjust_value" name="adjust_value" required>
                
                <button type="submit">Adjust</button>
            </form>
        </div>
        
        <div id="progressTracker" style="display: none;">
            <h2>Track Your Progress</h2>
            <form id="progressForm">
                <label for="goal">Goal:</label>
                <select id="goal" name="goal" required>
                    <option value="short_term">Short-term Goal</option>
                    <option value="long_term">Long-term Goal</option>
                </select>
                
                <label for="progress">Progress (%):</label>
                <input type="number" id="progress" name="progress" min="0" max="100" required>
                
                <button type="submit">Update Progress</button>
            </form>
        </div>
    </div>

    <script>
        let userId;
        let recommendationChart;

        document.getElementById('financialForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const response = await fetch('/submit', { method: 'POST', body: formData });
            const data = await response.json();
            userId = data.user_id;
            displayRecommendation(data.recommendation);
        });

        document.getElementById('adjustForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            formData.append('user_id', userId);
            const response = await fetch('/adjust', { method: 'POST', body: formData });
            const data = await response.json();
            if (data.success) {
                displayRecommendation(data.recommendation);
            } else {
                alert('Error: ' + data.error);
            }
        });

        document.getElementById('progressForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            formData.append('user_id', userId);
            const response = await fetch('/track_progress', { method: 'POST', body: formData });
            const data = await response.json();
            if (data.success) {
                alert('Progress updated successfully!');
            } else {
                alert('Error: ' + data.error);
            }
        });

        function displayRecommendation(recommendation) {
            document.getElementById('recommendation').style.display = 'block';
            document.getElementById('adjustments').style.display = 'block';
            document.getElementById('progressTracker').style.display = 'block';

            const ctx = document.getElementById('recommendationChart').getContext('2d');
            
            if (recommendationChart) {
                recommendationChart.destroy();
            }

            recommendationChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: Object.keys(recommendation),
                    datasets: [{
                        data: Object.values(recommendation),
                        backgroundColor: [
                            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                            '#FF9F40', '#FF6384', '#C9CBCF', '#7BC225'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Investment Allocation'
                    }
                }
            });
        }
    </script>
</body>
</html>
"""

print("AI Financial Advisor Flask application is ready to run!")
print("Make sure to create a 'templates' folder and place the HTML content in 'index.html' within that folder.")
print("Run this script and navigate to http://localhost:5000 in your web browser to use the application.")