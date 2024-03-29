import random
import yaml
from abc import ABC, abstractmethod
from pathlib import Path
from sdjquiz.vue.abstract_vue import QuizVue
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
        except QuizzError as error:
            raise error
        except OSError:
            raise QuizzError("Incorrect file path.")
        else:
            self.quiz = quiz

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

    def _play_quiz(self) -> None:
        """
        The quiz routine

        Returns:
            None
        """
        # Welcomes the user
        self.vue.show_greetings(self.quiz.title, self.quiz.description, self.quiz.questions_count,
                                self.quiz.max_score)

        # Ask the user how many questions he wants
        questions_count = self.vue.ask_questions_count(default_count=self.quiz.questions_count)

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

    def start(self) -> None:
        """
        Quiz entry point
        Loads quiz data from file or exit on error, and launches the quiz.

        Returns:
            None
        """
        # Clear the terminal
        self.vue.clear()

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
            exit(1)
        else:
            self._play_quiz()
