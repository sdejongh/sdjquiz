import yaml
from sdjquiz.model import Quiz, Question, Answer
from sdjquiz.exceptions import *
from sdjquiz.helpers import is_valid_input_count


class QuizController:
    def __init__(self, vue):
        self.vue = vue
        self.quiz = None
        self.question_count = 0

    def load_quiz(self, filepath: str) -> None:
        """Loads data from YAML file and creates the Quiz

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

    def start(self) -> None:
        try:
            self.load_quiz("c:/Users/steve/Projects/sdjquiz/samples/quiz_python.yaml")
        except QuizzError as err:
            self.vue.show_error(err)
            exit()
        else:
            self.vue.show_greetings(self.quiz.title, self.quiz.description, self.quiz.questions_count, self.quiz.max_score)
            user_input = None
            while not is_valid_input_count(user_input):
                user_input = self.vue.ask_questions_count(self.quiz.questions_count)
            self.question_count = int(user_input)

