# Import the datetime module to work with dates and times
import datetime

# Define a class named Publication. This is a blueprint for creating objects that represent publications.
class Publication:
    """
    Abstract base class for all types of publications.

    Attributes:
        text (str): The text of the publication.
    """
    # The __init__ method is a special method that is called when a new object is created from this class.
    # It initializes the object with the given text.
    def __init__(self, text):
        """
        Initialize a new publication with the given text.

        Args:
            text (str): The text of the publication.
        """
        self.text = text

    # The display method is a placeholder that must be implemented by any class that inherits from Publication.
    def display(self):
        """
        Abstract method to display the publication.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement display method.")

# Define a class named News that inherits from Publication. This class represents a news publication.
class News(Publication):
    """
    Represents a news publication.

    Attributes:
        location (str): The location where the news happened.
        publish_date (str): The date and time when the news was published.
    """
    # The __init__ method initializes the News object with the given text and location.
    # It also sets the publish date to the current date and time.
    def __init__(self, text, location):
        """
        Initialize a new news publication with the given text and location.

        Args:
            text (str): The text of the news.
            location (str): The location where the news happened.
        """
        super().__init__(text) # Call the __init__ method of the parent class to set the text.
        self.location = location
        self.publish_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # The display method returns a formatted string that represents the News object.
    def display(self):
        """
        Display the news publication.

        Returns:
            str: A formatted string representing the news publication.
        """
        return f"Type: News\nText: {self.text}\nLocation: {self.location}\nPublish Date: {self.publish_date}\n------------------------------------"

# Define a class named PrivateAd that inherits from Publication. This class represents a private ad publication.
class PrivateAd(Publication):
    """
    Represents a private ad publication.

    Attributes:
        expiration_date (datetime.date): The expiration date of the ad.
        days_left (int): The number of days left until the ad expires.
    """
    # The __init__ method initializes the PrivateAd object with the given text and expiration date.
    # It also calculates the number of days left until the ad expires.
    def __init__(self, text, expiration_date):
        """
        Initialize a new private ad publication with the given text and expiration date.

        Args:
            text (str): The text of the ad.
            expiration_date (datetime.date): The expiration date of the ad.
        """
        super().__init__(text) # Call the __init__ method of the parent class to set the text.
        self.expiration_date = expiration_date
        self.days_left = self.calculate_days_left()

    # The calculate_days_left method calculates and returns the number of days left until the ad expires.
    def calculate_days_left(self):
        """
        Calculate the number of days left until the ad expires.

        Returns:
            int: The number of days left until the ad expires.
        """
        today = datetime.datetime.now().date()
        return (self.expiration_date - today).days

    # The display method returns a formatted string that represents the PrivateAd object.
    def display(self):
        """
        Display the private ad publication.

        Returns:
            str: A formatted string representing the private ad publication.
        """
        return f"Type: Private Ad\nText: {self.text}\nExpiration Date: {self.expiration_date}\nDays Left: {self.days_left}\n------------------------------------"

# Define a class named QuoteOfTheDay that inherits from Publication. This class represents a quote of the day publication.
class QuoteOfTheDay(Publication):
    """
    Represents a quote of the day publication.

    Attributes:
        author (str): The author of the quote.
        date (str): The date when the quote was published.
        day_of_week (str): The day of the week when the quote was published.
    """
    # The __init__ method initializes the QuoteOfTheDay object with the given text and author.
    # It also sets the date and day of the week to the current date.
    def __init__(self, text, author):
        """
        Initialize a new quote of the day publication with the given text and author.

        Args:
            text (str): The text of the quote.
            author (str): The author of the quote.
        """
        super().__init__(text) # Call the __init__ method of the parent class to set the text.
        self.author = author
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.day_of_week = datetime.datetime.now().strftime("%A")

    # The display method returns a formatted string that represents the QuoteOfTheDay object.
    def display(self):
        """
        Display the quote of the day publication.

        Returns:
            str: A formatted string representing the quote of the day publication.
        """
        return f"Type: Quote of the Day\nText: {self.text}\nAuthor: {self.author}\nDate: {self.date}\nDay of the Week: {self.day_of_week}\n------------------------------------"

# Define a class named PublicationManager. This class manages the creation and publishing of publications.
class PublicationManager:
    """
    Manages the creation and publication of different types of publications.
    """
    # The create_publication method creates a publication based on the user's choice.
    @staticmethod
    def create_publication(choice):
        """
        Create a new publication based on the user's choice.

        Args:
            choice (str): The user's choice for the type of publication to create.

        Returns:
            Publication: A new publication object of the appropriate type.
            None: If the choice is invalid or an error occurs.
        """
        if choice.lower() == 'n':
            news_text = input("Please enter the news text: ")
            location = input("Please enter the location where this happened: ")
            return News(news_text, location)
        elif choice.lower() == 'a':
            ad_text = input("Please enter the advertisement text: ")
            expiration_date_str = input("Please enter the expiration date (YYYY-MM-DD): ")
            try:
                year, month, day = map(int, expiration_date_str.split('-'))
                expiration_date = datetime.date(year, month, day)
                return PrivateAd(ad_text, expiration_date)
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                return None
        elif choice.lower() == 'q':
            quote_text = input("Please enter the quote text: ")
            author = input("Please enter the author: ")
            return QuoteOfTheDay(quote_text, author)
        else:
            print("Invalid choice.")
            return None

    # The publish method publishes a publication based on the user's choice.
    @staticmethod
    def publish():
        """
        Publish a new publication based on the user's choice.

        This method prompts the user for input, creates a new publication, and writes it to 'news.txt'.
        """
        print("Welcome to the News Generator App!")
        choice = input("What do you want to publish? Press N for news, A for private ad, Q for quote of the day: ")
        publication = PublicationManager.create_publication(choice)
        if publication:
            with open("news.txt", "a") as file:
                file.write(publication.display() + "\n")
            print("Publication entry has been successfully added to 'news.txt'.")

# The main function that starts the application.
def main():
    """
    The main function that starts the application.
    """
    PublicationManager.publish()

# Check if this script is the main program and run the main function if it is.
if __name__ == "__main__":
    main()