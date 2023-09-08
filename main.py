import sqlite3

stephen_king_adaptations_list = []
with open('stephen_king_adaptations.txt', 'r') as file:
    for line in file:
        stephen_king_adaptations_list.append(line.strip())

conn = sqlite3.connect('stephen_king_adaptations.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
    movieID INTEGER PRIMARY KEY AUTOINCREMENT,
    movieName TEXT,
    movieYear INTEGER,
    imdbRating REAL
)
''')

for adaptation in stephen_king_adaptations_list:
    movie_data = adaptation.split(',')
    movie_name = movie_data[1]
    cursor.execute('SELECT movieName FROM stephen_king_adaptations_table WHERE movieName = ?', (movie_name,))
    existing_movie = cursor.fetchone()
    if not existing_movie:
        cursor.execute('INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating) VALUES (?, ?, ?)',
                       (movie_name, int(movie_data[2]), float(movie_data[3])))

conn.commit()

while True:
    print("\nChoose an option:")
    print("1. Search by movie name")
    print("2. Search by movie year")
    print("3. Search by movie rating")
    print("4. Quit")
    choice = input("Enter your choice : ")

    if choice == '1':
        movie_name = input("Enter the name of the movie: ")
        cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE movieName = ?', (movie_name,))
        event = cursor.fetchone()
        if event:
            print(f"Name: {event[1]}, Year: {event[2]}, Rating: {event[3]}")
        else:
            print("No movies found")

    elif choice == '2':
        movie_year = input("Enter the year of the movie: ")
        cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?', (int(movie_year),))
        events = cursor.fetchall()
        if events:
            for event in events:
                print(f"Name: {event[1]}, Year: {event[2]}, Rating: {event[3]}")
        else:
            print("No movies found")

    elif choice == '3':
        rating_limit = input("Enter the minimum rating: ")
        cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?', (float(rating_limit),))
        events = cursor.fetchall()
        if events:
            for event in events:
                print(f"Name: {event[1]}, Year: {event[2]}, Rating: {event[3]}")
        else:
            print("No movies found")

    elif choice == '4':
        break

conn.close()
