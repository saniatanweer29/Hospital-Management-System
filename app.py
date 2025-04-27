from flask import Flask, render_template, jsonify, request
import mysql.connector

app = Flask(__name__)

# Configure database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="javin1326",  # Your password
    database="hospital_management"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def home():
    try:
        query = "SELECT * FROM doctor"
        cursor.execute(query)
        doctors = cursor.fetchall()
        return render_template('index.html', doctors=doctors)
    except Exception as e:
        return f"Error loading doctors: {e}", 500

@app.route('/api/doctors')
def get_doctors():
    try:
        query = "SELECT * FROM doctor"
        cursor.execute(query)
        doctors = cursor.fetchall()
        return jsonify(doctors), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/patients')
def get_patients():
    try:
        query = "SELECT * FROM patient"
        cursor.execute(query)
        patients = cursor.fetchall()
        return jsonify(patients), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/rooms')
def get_rooms():
    try:
        query = "SELECT * FROM room"
        cursor.execute(query)
        rooms = cursor.fetchall()
        return jsonify(rooms), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/pharmacy')
def get_pharmacy():
    try:
        query = "SELECT * FROM pharmacy"
        cursor.execute(query)
        pharmacies = cursor.fetchall()
        return jsonify(pharmacies), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bills')    
def get_bills():
    try:
        query = "SELECT * FROM bills"
        cursor.execute(query)
        bills = cursor.fetchall()
        return jsonify(bills), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/patients/add', methods=['POST'])
def add_patient():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['name', 'gender', 'dob', 'mobile']
        if not all(field in data and str(data[field]).strip() for field in required_fields):
            return jsonify({"error": "All fields are required"}), 400

        name = data['name']
        gender = data['gender']
        dob = data['dob']
        mobile = data['mobile']

        # Insert into DB
        query = "INSERT INTO patient (name, gender, dob, mobile_no) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, gender, dob, mobile))
        db.commit()

        return jsonify({"message": "Patient added successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/rooms/add', methods=['POST'])
def add_room():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['room_no', 'room_type', 'status', 'price', 'facilities']
        if not all(field in data and str(data[field]).strip() for field in required_fields):
            return jsonify({"error": "All fields are required"}), 400

        room_no = data['room_no']
        room_type = data['room_type']
        status = data['status']
        price = data['price']
        facilities = data['facilities']

        # Insert into DB
        query = """
        INSERT INTO room (room_no, room_type, status, price, facilities)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (room_no, room_type, status, price, facilities))
        db.commit()

        return jsonify({"message": "Room added successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bills/add', methods=['POST'])
def add_bill():
    try:
        data = request.get_json()

        required_fields = ['patient_id', 'amount', 'name']
        if not all(field in data and str(data[field]).strip() for field in required_fields):
            return jsonify({"error": "All fields are required"}), 400

        query = "INSERT INTO bills (patient_id, amount, name) VALUES (%s, %s, %s)"
        cursor.execute(query, (data['patient_id'], data['amount'], data['name']))
        db.commit()

        return jsonify({"message": "Bill added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
