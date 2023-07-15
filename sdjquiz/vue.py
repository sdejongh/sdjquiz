from abc import ABC, abstractmethod
from rich.console import Console
from sdjquiz.model import Quiz


class QuizVue(ABC):
    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def show_error(self, message: str) -> None:
        pass

    @abstractmethod
    def show_greetings(self, quiz_title: str, quiz_description: str, quiz_questions_count: int, quiz_max_score: int):
        pass

    @abstractmethod
    def ask_questions_count(self, default_count: int) -> str:
        pass


class QuizTUI(QuizVue):
    def __init__(self):
        self.console = Console()

    def clear(self):
        self.console.clear()

    def show_error(self, message):
        self.console.print(f"ERROR: {message}")

    def show_greetings(self, quiz_title: str, quiz_description: str, quiz_questions_count: int, quiz_max_score: int):
        self.clear()
        self.console.print(f"Welcome to the quiz: {quiz_title.title()}")
        self.console.print(f"Description: {quiz_description.title()}")
        self.console.print(f"Number of questions: {quiz_questions_count}")
        self.console.print(f"Maximum score: {quiz_max_score}")
        self.console.print()

    def ask_questions_count(self, default_count: int) -> str:
        return self.console.input(f"How many questions (default: {default_count})")



