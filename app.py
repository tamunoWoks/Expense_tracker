# Install Flask
pip install flask

# Import modules
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Expense model for the database
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Expense {self.id}>'

# API to get all expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total_expense = sum(expense.amount for expense in expenses)
    expense_list = [{"id": expense.id, "description": expense.description, "amount": expense.amount, "date": expense.date} for expense in expenses]
    return jsonify({"expenses": expense_list, "total_expense": total_expense})

# API to add a new expense
@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    description = data.get('description', '')
    amount = data.get('amount', 0)
    
    if description and amount:
        try:
            new_expense = Expense(description=description, amount=float(amount))
            db.session.add(new_expense)
            db.session.commit()
            return jsonify({"message": "Expense added successfully!"}), 201
        except:
            return jsonify({"message": "Error adding expense"}), 500
    return jsonify({"message": "Invalid input"}), 400

# API to delete an expense
@app.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense_to_delete = Expense.query.get_or_404(id)
    try:
        db.session.delete(expense_to_delete)
        db.session.commit()
        return jsonify({"message": "Expense deleted successfully!"}), 200
    except:
        return jsonify({"message": "Error deleting expense"}), 500

# Serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
