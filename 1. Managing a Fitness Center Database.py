from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema, ValidationError
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    age = fields.String(required=True)

    class Meta:
        fields = ("id", "name", "phone")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)


def get_db_connection():
    db_name = "Gym_Database"
    user = "root"
    password = "*****"
    host = "localhost"

    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )
        if conn.is_connected():
            print("Connected to MySQL database successfully.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if conn and conn.is_connected():
            conn.close()
            print("My SQL connection is closed.")

@app.route('/Members', methods=['POST'])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 500
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Data connection failed"}), 500
        
        cursor = conn.cursor()

        new_member = (member_data['id'], member_data['name'], member_data['age'])

        query = "INSERT INTO Customers (id, name, age) VALUES (%s, %s, %s)"

        cursor.execute(query, new_member)
        conn.commit()

        return jsonify({"message": "New member added successfully"}), 201
    except ValidationError as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("My SQL connection is closed.")

@app.route('/Members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Data connection failed"}), 500
        
        cursor = conn.cursor()
        query = "SELECT * FROM Members where id = %s"

        cursor.execute(query, (id))
        member = cursor.fetchone()

        if member:
            return jsonify(members_schema.dump(member))
        else:
            return jsonify({"Error: Member not found."}), 404

    except ValidationError as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("My SQL connection is closed.")

@app.route('/Members/<int:id>', methods=['GET'])
def get_all_member(id):    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Data connection failed"}), 500
        
        cursor = conn.cursor()
        query = "SELECT * FROM Members"

        cursor.execute(query, (id))
        conn.commit()
        members = conn.fetchall()
        if members:
            return jsonify(members_schema.dump(members))
        else:
            return jsonify({"Error: No members have been added to the database."})
    except ValidationError as e:
        print(f"Error: {e}"), 500
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("My SQL connection is closed.")

@app.route('/Members/<int:id>', methods=['DELETE'])
def delete_member(id):    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Data connection failed"}), 500
        
        cursor = conn.cursor()
        query = "DELETE FROM Members WHERE id = %s"

        cursor.execute(query, (id))
        return jsonify({"message": "Member deleted successfully."}), 200

    except ValidationError as e:
        print(f"Error: {e}"), 500
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("My SQL connection is closed.")

@app.route('/Members/<int:id>', methods=['PUT'])
def update_member(id):    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Data connection failed"}), 500
        
        cursor = conn.cursor()
        query = "UPDATE Members SET name = %s, age= %s WHERE id = %s"

        cursor.execute(query, id, (data['name']), (data['id']))
        cursor.commit()
        return jsonify({"message": "Member information updated successfully."})

    except ValidationError as e:
        print(f"Error: {e}"), 500
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("My SQL connection is closed.")

class WorkoutSessionSchema(ma.Schema):
    session_id = fields.String(required=True)
    member_id = fields.String(required=True)
    session_date = fields.String(required=True)
    session_time = fields.String(required=True)
    activity= fields.String(required=True)

    class Meta:
        fields = ("session_id", "member_id", "session_date", "session_time", "activity")

WorkoutSession_schema = WorkoutSessionSchema()
WorkoutSessions_schema = WorkoutSessionSchema(many=True)

@app.route('/WorkoutSessions', methods=['POST'])
def add_workoutsession():
    try:
        workoutsession_data = WorkoutSession_schema.load(request.json)
    
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 500
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Data connection failed"}), 500
        
        cursor = conn.cursor()

        new_session = (workoutsession_data['id'], workoutsession_data['name'], workoutsession_data['age'])

        query = "INSERT INTO Customers (id, name, age) VALUES (%s, %s, %s)"

        cursor.execute(query, new_session)
        conn.commit()

        return jsonify({"message": "New workout session added successfully"}), 201
    except ValidationError as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("My SQL connection is closed.")

@app.route('/WorkoutSessions/<int:id>', methods=['GET'])
def get_workoutsession(session_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Data connection failed"}), 500
        
        cursor = conn.cursor()
        query = "SELECT * FROM Members where id = %s"

        cursor.execute(query, (session_id))
        session = cursor.fetchone()

        if session:
            return jsonify(WorkoutSession_schema.dump(session))
        else:
            return jsonify({"Error: Session not found."}), 404

    except ValidationError as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("My SQL connection is closed.")

@app.route('/WorkoutSession /<int:id>', methods=['PUT'])
def update_workout_session(id): 
    try:
        data = WorkoutSessions_schema.load(request.json)
    
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 500   
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Data connection failed"}), 500
        
        cursor = conn.cursor()
        query = "UPDATE WorkoutSession SET session_date = %s, session_time= %s, activity = %s WHERE session_id = %s"

        cursor.execute(query, id, (data['session_date']), (data['session_time']), (data['activity']))
        cursor.commit()
        return jsonify({"message": "Workout Session updated successfully."})

    except ValidationError as e:
        print(f"Error: {e}"), 500
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("My SQL connection is closed.")

@app.route('/WorkoutSession /<int:id>', methods=['GET'])
def workout_session_for_member(member_id):    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Data connection failed"}), 500
        
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM WorkoutSessions WHERE member_id = %s"

        cursor.execute(query, member_id)
        cursor.fetchall()
        return jsonify({"message": "Workout session for member found."})

    except ValidationError as e:
        print(f"Error: {e}"), 500
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("My SQL connection is closed.")