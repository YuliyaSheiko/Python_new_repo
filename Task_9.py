import datetime
import os
import csv
from Task_3 import normalize_text
import string
import json
import xml.etree.ElementTree as ET


class FileParser:
    @staticmethod
    def parse_input_file(file_path):
        publications = []
        try:
            with open(file_path, "r") as file:
                file_content = file.read()
                # Detect the file type based on its content
                if file_content.strip().startswith("{") and file_content.strip().endswith("}"):
                    # Assuming JSON format
                    data = json.loads(file_content)
                else:
                    # Assuming other formats
                    if file_path.endswith('.xml'):
                        # Parse XML
                        data = FileParser.parse_xml(file_path)
                    else:
                        # Assuming other formats, using eval()
                        data = eval(file_content)
                for item in data:
                    # Determine the type of publication and create the appropriate object
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

    @staticmethod
    def parse_xml(file_path):
        print('test!!!')
        data = []
        try:
            print("Attempting to parse XML file at:", file_path)
            root = None
            with open(file_path, 'r') as xml_file:
                for event, elem in ET.iterparse(xml_file):
                    if root is None:
                        root = elem
                    if elem.tag == 'publication':
                        item_data = {}
                        for child in elem:
                            if child.text is not None:
                                item_data[child.tag] = child.text
                            else:
                                print("Found NoneType for tag:", child.tag)
                                print("Child element:", ET.tostring(child))
                                item_data[child.tag] = ''
                        data.append(item_data)
                        root.clear()  # Clear the element to free memory

            print("XML content parsed successfully!")
        except Exception as e:
            print("An error occurred while parsing the XML file:", e)
        return data


class Publication:
    """
    Base class for all types of publications.

    Attributes:
        text (str): The text content of the publication.
    """

    def __init__(self, text):
        """
        Initialize the Publication with the given text.

        Args:
            text (str): The text content of the publication.
        """
        self.text = text

    def display(self):
        """
        Abstract method to display the publication.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement display method.")


class News(Publication):
    """
    Represents a news publication.

    Attributes:
        location (str): The location where the news is published.
        publish_date (str): The date and time when the news was published.
    """

    def __init__(self, text, location):
        """
        Initialize the News with the given text and location.

        Args:
            text (str): The text content of the news.
            location (str): The location where the news is published.
        """
        super().__init__(text)
        self.location = location
        self.publish_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def display(self):
        """
        Display the news publication details.

        Returns:
            str: A formatted string containing the news details.
        """
        return f"Type: News\nText: {self.text}\nLocation: {self.location}\nPublish Date: {self.publish_date}\n------------------------------------"


class PrivateAd(Publication):
    """
    Represents a private ad publication.

    Attributes:
        expiration_date (datetime.date): The expiration date of the ad.
        days_left (int): The number of days left until the ad expires.
    """

    def __init__(self, text, expiration_date):
        """
        Initialize the PrivateAd with the given text and expiration date.

        Args:
            text (str): The text content of the ad.
            expiration_date (datetime.date): The expiration date of the ad.

        Raises:
            ValueError: If the expiration date is not a future date.
        """
        super().__init__(text)
        if expiration_date <= datetime.date.today():
            raise ValueError("Expiration date must be a future date. Please enter a valid future date.")
        self.expiration_date = expiration_date
        self.days_left = self.calculate_days_left()

    def calculate_days_left(self):
        """
        Calculate the number of days left until the ad expires.

        Returns:
            int: The number of days left until the ad expires.
        """
        today = datetime.datetime.now().date()
        return (self.expiration_date - today).days

    def display(self):
        """
        Display the private ad publication details.

        Returns:
            str: A formatted string containing the ad details.
        """
        return f"Type: Private Ad\nText: {self.text}\nExpiration Date: {self.expiration_date}\nDays Left: {self.days_left}\n------------------------------------"


class QuoteOfTheDay(Publication):
    """
    Represents a quote of the day publication.

    Attributes:
        author (str): The author of the quote.
        date (str): The date when the quote was published.
        day_of_week (str): The day of the week when the quote was published.
    """

    def __init__(self, text, author):
        """
        Initialize the QuoteOfTheDay with the given text and author.

        Args:
            text (str): The text content of the quote.
            author (str): The author of the quote.
        """
        super().__init__(text)
        self.author = author
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.day_of_week = datetime.datetime.now().strftime("%A")

    def display(self):
        """
        Display the quote of the day publication details.

        Returns:
            str: A formatted string containing the quote details.
        """
        return f"Type: Quote of the Day\nText: {self.text}\nAuthor: {self.author}\nDate: {self.date}\nDay of the Week: {self.day_of_week}\n------------------------------------"


class PublicationManager:
    """
    Manages the creation and publication of various types of publications.

    This class provides methods for creating publications from user input,
    publishing them to a console or file, and saving statistics about the
    publications to CSV files.
    """
    DEFAULT_FOLDER = "./input_files/"  # Define the default folder for input files

    @staticmethod
    def create_publication_from_input(choice):
        """
        Creates a publication based on user input.

        Args:
            choice (str): The type of publication to create.
                'n' for news, 'a' for private ad, 'q' for quote of the day.

        Returns:
            A News, PrivateAd, or QuoteOfTheDay object based on the user's choice.
            Returns None if the choice is invalid.
        """
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
        """
        Publishes publications based on user input.

        This method prompts the user to choose how they want to publish
        (console or file) and then calls the appropriate method to handle
        the publication.
        """
        print("Welcome to the News Generator App!")
        choice = input("How do you want to publish? Press C for console, F for file: ")

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

                # Count words in news.txt and save to CSV
                PublicationManager.save_word_count_to_csv("news.txt", "word_count.csv")
                PublicationManager.save_letter_count_to_csv("news.txt", "word_count.csv")

        else:
            print("Invalid choice.")

    @staticmethod
    def publish_from_input():
        """
        Publishes a publication created from user input.

        This method prompts the user to choose the type of publication to create
        (news, private ad, quote of the day) and then creates the publication
        and adds it to 'news.txt'.
        """
        print("Welcome to the News Generator App!")
        choice = input("What do you want to publish? Press N for news, A for private ad, Q for quote of the day: ")
        publication = PublicationManager.create_publication_from_input(choice)
        if publication:
            with open("news.txt", "a") as file:
                file.write(publication.display() + "\n")
            print("Publication entry has been successfully added to 'news.txt'.")

            # Count words in news.txt and save to CSV
            PublicationManager.save_word_count_to_csv("news.txt", "word_count.csv")
            PublicationManager.save_letter_count_to_csv("news.txt", "letter_stats.csv")

    @staticmethod
    def save_word_count_to_csv(input_file, output_file):
        """
        Counts the occurrences of each word in the input file and saves the counts to a CSV file.

        Args:
            input_file (str): The path to the input file.
            output_file (str): The path to the output CSV file.
        """
        word_counts = {}
        with open(input_file, "r") as file:
            words = file.read().lower().split()
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1

        with open(output_file, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            for word, count in word_counts.items():
                writer.writerow([word, count])  # Write word-count pair

        print(f"Word count has been saved to '{output_file}'.")

    @staticmethod
    def save_letter_count_to_csv(input_file, output_file):
        """
        Counts the occurrences of each letter in the input file and saves the counts to a CSV file.

        Args:
            input_file (str): The path to the input file.
            output_file (str): The path to the output CSV file.
        """
        # Initialize counts for each letter
        letter_counts = {letter: 0 for letter in string.ascii_lowercase}
        total_letter_count = 0

        # Read the input file and count occurrences of each letter
        with open(input_file, "r") as file:
            text = file.read().lower()
            for char in text:
                if char in string.ascii_lowercase:
                    letter_counts[char] += 1
                    total_letter_count += 1

        # Write the results to the output CSV file
        with open(output_file, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Letter", "Count", "Percentage"])
            for letter in string.ascii_lowercase:
                count = letter_counts[letter]
                percentage = (count / total_letter_count) * 100 if total_letter_count > 0 else 0
                writer.writerow([letter, count, f"{percentage:.2f}%"])

        print(f"Letter count has been saved to '{output_file}'.")


def main():
    """
    The main entry point of the application.

    This function calls the publish method to start the publication process.
    """
    PublicationManager.publish()


if __name__ == "__main__":
    main()