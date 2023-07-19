from abc import ABC, abstractmethod
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm


class QuizVue(ABC):

    @abstractmethod
    def ask_file_path(self) -> str:
        """
        Ask user for a path to the quiz data file and returns it.

        Returns:
            str:    the path to the file (can be absolute or relative)
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clears the screen

        Returns:
            None
        """
        pass

    @abstractmethod
    def pause(self) -> None:
        """
        Mark a pause (ie: ask user to press a key or anything like that).

        Returns:
            None
        """
        pass

    @abstractmethod
    def show_error(self, message: str or Exception) -> None:
        """
        Display error message to the user
        Args:
            message: the error message

        Returns:
            None
        """
        pass

    @abstractmethod
    def show_greetings(self, quiz_title: str, quiz_description: str, quiz_questions_count: int, quiz_max_score: int) -> None:
        """
        Welcomes the user and shows basic information about the quiz
        Args:
            quiz_title:             the quiz title
            quiz_description:       the quiz description
            quiz_questions_count:   the number of questions in the quiz
            quiz_max_score:         the maximum score of the quiz

        Returns:
            None
        """
        pass

    @abstractmethod
    def ask_questions_count(self, default_count: int) -> int:
        """
        Asks the user how many questions he wants to answer.

        Args:
            default_count:  the default number of questions

        Returns:
            int:    the number of questions
        """
        pass

    @abstractmethod
    def show_question(self, question_index: int, title: str, text: str, answers: list[str], correct_count: int) -> None:
        """
        Displays the question to the user

        Args:
            question_index: the question index (number x of y in quiz)
            title:          the title of the question
            text:           the body of the question
            answers:        the list of answers
            correct_count:  the number of correct answers

        Returns:
            None
        """
        pass

    @abstractmethod
    def ask_answer(self) -> str:
        """
        Asks and returns the user answer
        The answer should be formatted as a string of digits separated by comas.
        examples:
            1 answer:   1 or 2 or 5
            2 answers:  1,3 or 7,8
            3 answers:  1,5,9 or 7,8,9

        Returns:
            str: the user answer
        """
        pass

    @abstractmethod
    def show_result(self, quiz_title: str, score: int, max_score: int) -> None:
        """
        Displays the result of the quiz

        Args:
            quiz_title:     the quiz title
            score:          the score of the user
            max_score:      the maximum score

        Returns:
            None
        """
        pass


class QuizTUI(QuizVue):
    def __init__(self):
        self.console = Console()

    def ask_file_path(self) -> str:
        """
        Ask user for a path to the quiz data file and returns it.

        Returns:
            str:    the path to the file (can be absolute or relative)
        """
        self.console.print("Welcome to SDJQUIZ...")
        return Prompt.ask(console=self.console, prompt="Enter the path to the quiz file")

    def clear(self):
        """
        Clears the screen

        Returns:
            None
        """
        self.console.clear()

    def show_error(self, message: str or Exception):
        """
        Display error message to the user
        Args:
            message: the error message

        Returns:
            None
        """
        self.console.print(f"ERROR: {message}")

    def show_greetings(self, quiz_title: str, quiz_description: str, quiz_questions_count: int, quiz_max_score: int):
        """
        Welcomes the user and shows basic information about the quiz
        Args:
            quiz_title:             the quiz title
            quiz_description:       the quiz description
            quiz_questions_count:   the number of questions in the quiz
            quiz_max_score:         the maximum score of the quiz

        Returns:
            None
        """
        self.clear()
        self.console.print(f"Welcome to the quiz: {quiz_title.title()}")
        self.console.print(f"Description: {quiz_description.title()}")
        self.console.print(f"Number of questions: {quiz_questions_count}")
        self.console.print(f"Maximum score: {quiz_max_score}")
        self.console.line()

    def ask_questions_count(self, default_count: int) -> int:
        """
        Asks the user how many questions he wants to answer.

        Args:
            default_count:  the default number of questions

        Returns:
            int:    the number of questions as a string
        """
        return IntPrompt.ask(console=self.console, prompt="How many questions do you want ?")

    def pause(self) -> None:
        """
        Mark a pause (ie: ask user to press a key or anything like that).

        Returns:
            None
        """
        self.console.line()
        Prompt.ask(prompt="Press ENTER to continue...", console=self.console)

    def show_question(self, question_index: int, title: str, text: str, answers: list[str], correct_count: int) -> None:
        """
        Displays the question to the user

        Args:
            question_index: the question index (number x of y in quiz)
            title:          the title of the question
            text:           the body of the question
            answers:        the list of answers
            correct_count:  the number of correct answers

        Returns:
            None
        """
        self.clear()
        self.console.print(f"----[ Q{question_index+1:3d} : {title} ]----")
        self.console.print(text)
        self.console.line()
        self.console.print(f"Answers (select {correct_count}):")

        for idx, answer in enumerate(answers):
            self.console.print(f"{idx+1}) {answer}")

        self.console.line()

    def ask_answer(self) -> str:
        """
        Asks and returns the user answer
        The answer should be formatted as a string of digits separated by comas.
        examples:
            1 answer:   1 or 2 or 5
            2 answers:  1,3 or 7,8
            3 answers:  1,5,9 or 7,8,9

        Returns:
            str: the user answer
        """
        return Prompt.ask(console=self.console, prompt="Your answer (ie: 1 or 1,3,7)")

    def show_result(self, quiz_title: str, score: int, max_score: int) -> None:
        """
        Displays the result of the quiz

        Args:
            quiz_title:     the quiz title
            score:          the score of the user
            max_score:      the maximum score

        Returns:
            None
        """
        self.clear()
        self.console.print(f"Your result for quiz : {quiz_title}")
        self.console.line()
        self.console.print(f"You achieved a score of {score}/{max_score} ({100*score/max_score:.2f}%)")
        self.pause()
