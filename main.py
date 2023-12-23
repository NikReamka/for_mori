import sqlite3


class Library:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_books_table()

    def create_books_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                description TEXT,
                genre TEXT
            )
        ''')
        self.conn.commit()

    def add_book(self, title, author, description, genre):
        self.cursor.execute('''
            INSERT INTO books (title, author, description, genre)
            VALUES (?, ?, ?, ?)
        ''', (title, author, description, genre))
        self.conn.commit()

    def view_genres(self):
        self.cursor.execute('SELECT genre FROM books LIMIT 10')
        genres = self.cursor.fetchall()
        if genres != []:
            print('Уже добавленные жанры:')
            for genre in genres:
                print(f"{genre[0].capitalize()}")

    def select_book_by_id(self, number):
        self.cursor.execute('SELECT * FROM books WHERE id=?', (number, ))
        return self.cursor.fetchone()

    def view_books(self, dop_action):
        self.cursor.execute('SELECT id, title, author FROM books')
        books = self.cursor.fetchall()
        for book in books:
            print(f"{book[0]}. {book[1]} {book[2].capitalize()}")
        if dop_action == '1': #если действие не удаление книги
            action = input('Введите номер книги если хотите узнать подробную информацию про нее, если нет то введите 0: ')
            if action != '0':
                info = self.select_book_by_id(action)
                print(f"{info[1]} {info[2].capitalize()}")
                print(f"{info[4]}\n{info[3]}")
                

    def view_books_by_genre(self, genre):
        self.cursor.execute('SELECT id, title, author FROM books WHERE genre = ?', (genre.lower(),))
        books = self.cursor.fetchall()
        for book in books:
            print(f"{book[0]}. {book[1]} {book[2].capitalize()}")
        action = input('Введите номер книги если хотите узнать подробную информацию про нее, если нет то введите 0: ')
        if action != '0':
            info = self.select_book_by_id(action)
            print(f"{info[1]} {info[2].capitalize()}")
            print(f"{info[4]}\n{info[3]}")

    def search_books(self, keyword):
        search_param = '%' + keyword.lower() + '%'
        self.cursor.execute('SELECT id, title, author FROM books WHERE title LIKE ? OR author LIKE ? OR description LIKE ?', (search_param, search_param, search_param))
        books = self.cursor.fetchall()
        if books:
            for book in books:
                print(f"{book[0]}. {book[1]} {book[2].capitalize()}")
        else:
            print("Результат по вашему запросу не найден")

    def remove_book(self, book_id):
        self.cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        self.conn.commit()
        print("Книга удалена")

    def close(self):
        self.conn.close()

def main():
    db_name = "library.db"  # Имя файла базы данных SQLite
    library = Library(db_name)

    while True:
        print("\nУправление библиотекой")
        print("1. Добавить книгу")
        print("2. Список книг")
        print("3. Поиск книги")
        print("4. Удалить книгу")
        print("5. Выйти")

        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора: ")
            description = input("Введите описание: ")
            library.view_genres()
            genre = input("Введите жанр: ")
            library.add_book(title.lower(), author.lower(), description.lower(), genre.lower()) 
            print("Книга успешно добавлена")

        elif choice == '2':
            search_action = input('1. Общий список книг\n2. Список книг по жанру\nВыберите пункт: ')
            if search_action == '1':
                library.view_books('1') 
            elif search_action == '2':
                genre = input("Введите жанр: ")
                library.view_books_by_genre(genre)

        elif choice == '3':
            keyword = input("Введите слово для поиска: ")
            library.search_books(keyword)

        elif choice == '4':
            library.view_books('0')
            book_id = input("Введите айди книги для удаления: ")
            library.remove_book(book_id)

        elif choice == '5':
            print("Выход из системы управления библиотекой")
            library.close()
            break

        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()
