from mysql.connector import Error

class Student:
    @staticmethod
    def get_all(conn):
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM Students')
            students = cursor.fetchall()
            cursor.close()
            return students
        except Error as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_by_id(conn, student_id):
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM Students WHERE StudentID = %s', (student_id,))
            student = cursor.fetchone()
            cursor.close()
            return student
        except Error as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def create(conn, data):
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Students (Name, Age, Level, PhoneNumber)
                VALUES (%s, %s, %s, %s)
            ''', (data['Name'], data['Age'], data['Level'], data['PhoneNumber']))
            
            conn.commit()
            student_id = cursor.lastrowid
            cursor.close()
            return student_id
        except Error as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def update(conn, student_id, data):
        try:
            cursor = conn.cursor()
            
            # Build update query dynamically
            fields = []
            values = []
            
            for field in ['Name', 'Age', 'Level', 'PhoneNumber']:
                if field in data:
                    fields.append(f"{field} = %s")
                    values.append(data[field])
            
            if not fields:
                cursor.close()
                return False
            
            values.append(student_id)
            
            cursor.execute(f'''
                UPDATE Students
                SET {", ".join(fields)}
                WHERE StudentID = %s
            ''', values)
            
            conn.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def delete(conn, student_id):
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Students WHERE StudentID = %s', (student_id,))
            conn.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False