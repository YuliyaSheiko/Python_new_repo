import datetime
import os
from Task_3 import normalize_text


class FileParser:
    @staticmethod
    def parse_input_file(file_path):
        publications = []
        try:
            with open(file_path, "r") as file:
                data = eval(file.read())  # Safely evaluate the string as Python expression
                for item in data:
                    if item.get('type', '').lower() == 'n':
                        # Normalize the news text
                        normalized_text = normalize_text(item.get('text', ''))
                        publication = News(normalized_text, item.get('location', ''))
                    elif item.get('type', '').lower() == 'a':
                        expiration_date_str = item.get('expiration_date', '')
                        try:
                            year, month, day = map(int, expiration_date_str.split('-'))
                            expiration_date = datetime.date(year, month, day)
                            # Normalize the advertisement text
                            normalized_text = normalize_text(item.get('text', ''))
                            publication = PrivateAd(normalized_text, expiration_date)
                        except (ValueError, IndexError):
                            print("Invalid date format or expiration date is not provided correctly.")
                            continue
                    elif item.get('type', '').lower() == 'q':
                        # Normalize the quote text
                        normalized_text = normalize_text(item.get('text', ''))
                        publication = QuoteOfTheDay(normalized_text, item.get('author', ''))
                        publication.day_of_week = item.get('day_of_week',
                                                           '')  # Include the day_of_week property from the file
                    else:
                        print("Invalid publication type in the file.")
                        continue

                    publications.append(publication)
        except FileNotFoundError:
            print("File not found. Please provide a valid file path.")
        except Exception as e:
            print("An error occurred while parsing the file:", e)

        return publications


class Publication:
    def __init__(self, text):
        self.text = text

    def display(self):
        raise NotImplementedError("Subclasses must implement display method.")


class News(Publication):
    def __init__(self, text, location):
        super().__init__(text)
        self.location = location
        self.publish_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def display(self):
        return f"Type: News\nText: {self.text}\nLocation: {self.location}\nPublish Date: {self.publish_date}\n------------------------------------"


class PrivateAd(Publication):
    def __init__(self, text, expiration_date):
        super().__init__(text)
        if expiration_date <= datetime.date.today():
            raise ValueError("Expiration date must be a future date. Please enter a valid future dat")
        self.expiration_date = expiration_date
        self.days_left = self.calculate_days_left()

    def calculate_days_left(self):
        today = datetime.datetime.now().date()
        return (self.expiration_date - today).days

    def display(self):
        return f"Type: Private Ad\nText: {self.text}\nExpiration Date: {self.expiration_date}\nDays Left: {self.days_left}\n------------------------------------"


class QuoteOfTheDay(Publication):
    def __init__(self, text, author):
        super().__init__(text)
        self.author = author
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.day_of_week = datetime.datetime.now().strftime("%A")

    def display(self):
        return f"Type: Quote of the Day\nText: {self.text}\nAuthor: {self.author}\nDate: {self.date}\nDay of the Week: {self.day_of_week}\n------------------------------------"


class PublicationManager:
    DEFAULT_FOLDER = "./input_files/"  # Define the default folder for input files

    @staticmethod
    def create_publication_from_input(choice):
        if choice.lower() == 'n':
            news_text = input("Please enter the news text: ")
            location = input("Please enter the location where this happened: ")
            # Normalize the news text
            normalized_text = normalize_text(news_text)
            return News(normalized_text, location)
        elif choice.lower() == 'a':
            while True:
                ad_text = input("Please enter the advertisement text: ")
                expiration_date_str = input("Please enter the expiration date (YYYY-MM-DD): ")
                try:
                    year, month, day = map(int, expiration_date_str.split('-'))
                    expiration_date = datetime.date(year, month, day)
                    # Normalize the advertisement text
                    normalized_text = normalize_text(ad_text)
                    return PrivateAd(normalized_text, expiration_date)
                except ValueError:
                    print(
                        "Invalid date format or expiration date is not a future date. Please enter the date in YYYY-MM-DD format and ensure it's in the future.")
                except ValueError as e:
                    print(e)
                    continue
        elif choice.lower() == 'q':
            quote_text = input("Please enter the quote text: ")
            author = input("Please enter the author: ")
            # Normalize the quote text
            normalized_text = normalize_text(quote_text)
            return QuoteOfTheDay(normalized_text, author)
        else:
            print("Invalid choice.")
            return None

    @staticmethod
    def publish():
        print("Welcome to the News Generator App!")
        choice = input("How do you want to publish? Press C for manual input, F from file: ")

        if choice.lower() == 'c':
            PublicationManager.publish_from_input()
        elif choice.lower() == 'f':
            file_path = input("Please provide the file path or press Enter to use the default folder: ")
            if not file_path:
                file_path = PublicationManager.DEFAULT_FOLDER + input("Please provide the file name: ")
            publications = FileParser.parse_input_file(file_path)
            if publications:
                for publication in publications:
                    with open("news.txt", "a") as file:
                        file.write(publication.display() + "\n")
                print("Publications have been successfully added to 'news.txt'.")
                # Delete the file after successful parsing
                os.remove(file_path)
        else:
            print("Invalid choice.")

    @staticmethod
    def publish_from_input():
        print("Welcome to the News Generator App!")
        choice = input("What do you want to publish? Press N for news, A for private ad, Q for quote of the day: ")
        publication = PublicationManager.create_publication_from_input(choice)
        if publication:
            with open("news.txt", "a") as file:
                file.write(publication.display() + "\n")
            print("Publication entry has been successfully added to 'news.txt'.")


def main():
    PublicationManager.publish()


if __name__ == "__main__":
    main()