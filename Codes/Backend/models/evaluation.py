from mysql.connector import Error

class Evaluation:
    @staticmethod
    def get_all(conn):
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM Evaluations')
            evaluations = cursor.fetchall()
            cursor.close()
            return evaluations
        except Error as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_by_id(conn, evaluation_id):
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM Evaluations WHERE EvaluationID = %s', (evaluation_id,))
            evaluation = cursor.fetchone()
            cursor.close()
            return evaluation
        except Error as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_by_student(conn, student_id):
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM Evaluations WHERE StudentID = %s', (student_id,))
            evaluations = cursor.fetchall()
            cursor.close()
            return evaluations
        except Error as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def create(conn, data):
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Evaluations (StudentID, Date, Score, Notes)
                VALUES (%s, %s, %s, %s)
            ''', (data['StudentID'], data['Date'], data['Score'], data.get('Notes', '')))
            
            conn.commit()
            evaluation_id = cursor.lastrowid
            cursor.close()
            return evaluation_id
        except Error as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def update(conn, evaluation_id, data):
        try:
            cursor = conn.cursor()
            
            # Build update query dynamically
            fields = []
            values = []
            
            for field in ['StudentID', 'Date', 'Score', 'Notes']:
                if field in data:
                    fields.append(f"{field} = %s")
                    values.append(data[field])
            
            if not fields:
                cursor.close()
                return False
            
            values.append(evaluation_id)
            
            cursor.execute(f'''
                UPDATE Evaluations
                SET {", ".join(fields)}
                WHERE EvaluationID = %s
            ''', values)
            
            conn.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def delete(conn, evaluation_id):
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Evaluations WHERE EvaluationID = %s', (evaluation_id,))
            conn.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False