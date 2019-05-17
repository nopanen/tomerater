class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("Updated email for user {} to {}".format(self.name, self.email))

    def __repr__(self):
        return "User {}, email:	{},	books read:	{}".format(self.name, self.email, len(self.books))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

    def read_book(self, book, rating = None):
        self.books[book] = rating

    def get_average_rating(self):
        ratingssum = sum([rating for rating in self.books.values() if rating != None])
        return ratingssum / len(self.books)


class Book:
    def __init__(self, title, isbn, price):
        self.title = title
        self.isbn = isbn
        self.ratings = []
        self.price = price

    def get_title(self):
        return self.title
    
    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn
        print("Set ISBN for Book {} to {}".format(self.title, self.isbn))

    def add_rating(self, rating):
        if rating is None:
            print("No rating for the book " + self.title)
        elif rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")
    
    def __eq__(self, another_book):
        return self.title == another_book.title and self.isbn == another_book.isbn

    def get_average_rating(self):
        ratingssum = sum([rating for rating in self.ratings])
        return ratingssum / len(self.ratings)

    def	__hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "Book: {}, Isbn: {}, Ratings: {}".format(self.title, self.isbn, len(self.ratings))


class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        Book.__init__(self, title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author
    
    def __repr__(self):
        return self.title + " by " + self.author

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        Book.__init__(self, title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{},	a {} manual on	{}".format(self.title, self.level, self.subject)


class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn, price):
        if isbn not in [book.isbn for book in self.books.keys()]:
            return Book(title, isbn, price)
        print("Cannot create book. Book with supplied ISBN already exists.")

    def create_novel(self, title, author, isbn, price):
        if isbn not in [book.isbn for book in self.books.keys()]:
            return Fiction(title, author, isbn, price)
        print("Cannot create book. Book with supplied ISBN already exists.")

    def create_non_fiction(self, title, subject, level, isbn, price):
        if isbn not in [book.isbn for book in self.books.keys()]:
            return Non_Fiction(title, subject, level, isbn, price)
        print("Cannot create book. Book with supplied ISBN already exists.")

    def add_book_to_user(self, book, email, rating = None):
        if email not in self.users:
            print("No user with email {}!".format(email))
        else:
            user = self.users[email]
            user.read_book(book, rating)            
            book.add_rating(rating)
            
            if book not in self.books:
                self.books[book] = 1
            else:
                self.books[book] += 1

    def add_user(self, name, email, user_books = None):
        if email in self.users:
            print("The user with email {} already exists!".format(email))
            return None
        if "@" in email and (".com" in email or ".edu" in email or ".org" in email):
            self.users[email] = User(name, email)        
            if user_books:
                for user_book in user_books:
                    self.add_book_to_user(user_book, email)
        else:
            print("Cannot add user, email is not valid")

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        most_read_book = None
        most_read_book_times_read = 0
        
        for book, timesread in self.books.items():
            if timesread > most_read_book_times_read:
                most_read_book = book
                most_read_book_times_read = timesread

        return most_read_book

    def highest_rated_book(self):
        highest_rating = 0
        highest_rated_book = None
        
        for book in self.books.keys():
            rating = book.get_average_rating()
            if rating > highest_rating:
                highest_rating = rating
                highest_rated_book = book

        return highest_rated_book

    def most_positive_user(self):
        highest_rating = 0
        highest_rated_user = None
        
        for user in self.users.values():
            avg_rating = user.get_average_rating()
            if avg_rating > highest_rating:
                highest_rating = avg_rating
                highest_rated_user = user

        return highest_rated_user

    def get_n_most_read_books(self, n):   
        sortedlist = sorted(self.books.items(), key=lambda kv: kv[1], reverse=True)
        return sortedlist[:n]

    def get_n_most_prolific_readers(self, n):        
        newdict = {user.name:len(user.books) for user in self.users.values()}
        sortedlist = sorted(newdict.items(), key=lambda kv: kv[1], reverse=True)
        return sortedlist[:n]

    def get_n_most_expensive_books(self, n):
        newdict = {book.title:book.price for book in self.books.keys()}
        sortedlist = sorted(newdict.items(), key=lambda kv: kv[1], reverse=True)
        return sortedlist[:n]

    def get_worth_of_user(self,	user_email):
        if user_email not in self.users.keys():
            print("Cannot get worth of user. User {} is not found from list of users".format(user_email))
        else:
            user = self.users[user_email]
            return sum([book.price for book in user.books])