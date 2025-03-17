from mysql.connector import Error

class Plan:
    @staticmethod
    def get_all(conn):
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM Plans')
            plans = cursor.fetchall()
            cursor.close()
            return plans
        except Error as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_by_id(conn, plan_id):
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM Plans WHERE PlanID = %s', (plan_id,))
            plan = cursor.fetchone()
            cursor.close()
            return plan
        except Error as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_by_student(conn, student_id):
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM Plans WHERE StudentID = %s', (student_id,))
            plans = cursor.fetchall()
            cursor.close()
            return plans
        except Error as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def create(conn, data):
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Plans (StudentID, StartDate, EndDate, Status, Description)
                VALUES (%s, %s, %s, %s, %s)
            ''', (data['StudentID'], data['StartDate'], data['EndDate'], 
                  data['Status'], data.get('Description', '')))
            
            conn.commit()
            plan_id = cursor.lastrowid
            cursor.close()
            return plan_id
        except Error as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def update(conn, plan_id, data):
        try:
            cursor = conn.cursor()
            
            # Build update query dynamically
            fields = []
            values = []
            
            for field in ['StudentID', 'StartDate', 'EndDate', 'Status', 'Description']:
                if field in data:
                    fields.append(f"{field} = %s")
                    values.append(data[field])
            
            if not fields:
                cursor.close()
                return False
            
            values.append(plan_id)
            
            cursor.execute(f'''
                UPDATE Plans
                SET {", ".join(fields)}
                WHERE PlanID = %s
            ''', values)
            
            conn.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def delete(conn, plan_id):
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Plans WHERE PlanID = %s', (plan_id,))
            conn.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False