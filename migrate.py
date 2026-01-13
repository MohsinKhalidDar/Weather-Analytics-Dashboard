from storage.database import get_connection

def main():
    conn = get_connection()
    conn.close()
    print("Migration completed successfully!")

if __name__ == "__main__":
    main()
