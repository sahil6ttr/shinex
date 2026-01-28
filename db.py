import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="H@mesh@6@@gey",
        database="shinex"
    )
    return connection


if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✅ MySQL Connected Successfully!")
        conn.close()
    except Exception as e:
        print("❌ Connection Failed:", e)
