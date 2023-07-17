import random
import yaml
import re
from abc import ABC, abstractmethod
from pathlib import Path
from sdjquiz.vue import QuizTUI, QuizVue
from sdjquiz.model import Quiz
from sdjquiz.exceptions import *


class QuizController(ABC):

    vue: QuizVue
    quiz_file: Path

    def __init__(self):
        self.quiz = None
        self.vue = self.get_quiz_controller_vue()

    @abstractmethod
    def get_quiz_controller_vue(self) -> QuizVue:
        """
        Sets the QuizVue to use
        Returns:
            QuizVue():    The QuizVue subclass to use as vue
        """
        pass

    def load_quiz(self, filepath: Path) -> None:
        """
        Loads data from YAML file and creates the Quiz

        Args:
            filepath (str):         filepath of the yaml quiz file

        Returns:
            None
        """
        try:
            with open(filepath) as quiz_file:
                quiz_data = yaml.load(quiz_file, yaml.Loader)
                quiz = Quiz.from_dict(quiz_data)
        except FileNotFoundError:
            raise QuizzError(f"File {filepath} not found.")
        except PermissionError:
            raise QuizzError(f"Could not load data from {filepath}: permissions error")
        except yaml.YAMLError:
            raise QuizzError(f"Could not load data from {filepath}: YAML error")
        else:
            self.quiz = quiz

    @staticmethod
    def is_valid_input_count(text_input: str or None) -> bool:
        """
        Checks whether the input text is either a digit expression or an empty string.
        Args:
            text_input (str):   the text string to check

        Returns:
            bool:               True if the string is a digit expression or an empty string, else False
        """
        if text_input is None:
            return False
        return text_input.isdigit() or text_input == ""

    @abstractmethod
    def get_user_answer(self, answers_count: int, correct_count: int) -> set[int]:
        """
        Ask the user answer(s) and returns a set of values.

        Args:
            answers_count:  the number of answers shown
            correct_count:  the number of correct answers

        Returns:
            set[int]:       the set of user answers
        """
        pass

    def start(self) -> None:
        """
        Starts the Quiz main routine

        Returns:
            None
        """
        # Ask user for a quiz file
        filepath = self.vue.ask_file_path()

        # Expand or resolve relative path
        if filepath.startswith("~"):
            self.quiz_file = Path(filepath).expanduser()
        else:
            self.quiz_file = Path(filepath).resolve()

        # Load quiz from file or exit on error.
        try:
            self.load_quiz(self.quiz_file)
        except QuizzError as err:
            self.vue.show_error(err)
            exit()
        else:
            # Welcomes the user
            self.vue.show_greetings(self.quiz.title, self.quiz.description, self.quiz.questions_count,
                                    self.quiz.max_score)

            # Ask the user how many questions he wants
            user_input = None
            while not QuizController.is_valid_input_count(user_input):
                user_input = self.vue.ask_questions_count(self.quiz.questions_count)

            # Defaults to the maximum if no answer given
            questions_count = int(user_input) if user_input else self.quiz.questions_count

            # Get the list of questions
            questions = self.quiz.get_questions(questions_count)

            # Initialize the user score
            score = 0
            max_score = sum(question.score for question in questions)

            # Ask selected questions
            for idx, question in enumerate(questions):
                self.vue.clear()

                # Randomize answers order
                answers = question.answers
                random.shuffle(answers)

                # Create a set of correct answers index
                correct = set([idx for idx, answer in enumerate(answers) if answer.correct])

                # Display the question
                self.vue.show_question(idx, question.title, question.text, [answer.text for answer in answers],
                                       len(correct))

                # Get answer from user (should retard a set of answer indexes)
                user_answer = self.get_user_answer(len(answers), len(correct))

                # If sets matches add question score to the total
                if user_answer == correct:
                    score += question.score

                # Mark a pause
                self.vue.pause()

            # Displays the results
            self.vue.show_result(self.quiz.title, score, max_score)


class ConsoleQuizController(QuizController):

    def get_quiz_controller_vue(self) -> QuizVue:
        """
        Sets the QuizVue to use
        Returns:
            QuizVue():    The QuizVue subclass to use as vue
        """
        return QuizTUI()

    def get_user_answer(self, answers_count: int, correct_count: int) -> set[int]:
        """
        Ask the user answer(s) and returns a set of values.

        Args:
            answers_count:  the number of answers shown
            correct_count:  the number of correct answers

        Returns:
            set[int]:       the set of user answers
        """
        user_answer = None
        while not ConsoleQuizController.is_valid_answer(user_answer, answers_count, correct_count):
            user_answer = self.vue.ask_answer()
        user_answer = set(int(value) - 1 for value in user_answer.split(","))
        return user_answer

    @staticmethod
    def is_valid_answer(text_string: str or None, max_index: int, values: int) -> bool:
        """
        Checks if the text string is a valid user answer (1,2,3 for example)
        Must be comma separated digits

        Args:
            text_string (str):  the string to check
            max_index (int):    the highest index that can be found in the answer
            values (int):       the number of answers that must be provided

        Returns:
            bool:               Whether the string is valid or not
        """
        additional_values = "{" + str(values-1) + "}"
        if text_string is None or re.match(f"^[1-{max_index}](,[1-{max_index}]){additional_values}$", text_string) is None:
            return False
        return True
