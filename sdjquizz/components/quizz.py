import yaml
from sdjquizz.components.question import Answer, Question, QuestionType, get_question
from pathlib import Path
from random import shuffle


class UnableToLoadQuizz(Exception):
    pass


def load_from_file(filepath: str) -> dict or None:
    """
    Open the given YAML file path and tries to load its content.
    Args:
        filepath (str): relative or absolute path to the yaml file

    Returns:
        dict:   The YAML file content
    """
    file = Path(filepath).expanduser()
    try:
        with open(file) as datafile:
            data = yaml.load(datafile, yaml.Loader)
    except FileNotFoundError:
        return None
    except PermissionError:
        return None
    except yaml.YAMLError:
        return None
    else:
        return data


class Quizz:
    """Main Quizz class"""
    def __init__(self, shuffle_questions=True, show_explanations=False):
        self.meta = {}
        self.questions = []
        self.shuffle_questions = shuffle_questions
        self.max_score = 0
        self.current_score = 0
        self.current_question = 0
        self.show_explanation = show_explanations

    def load(self, filepath: str) -> int:
        """Loads quizz data from YAML file
        Adds each question to the Quizz.questions attribute.
        Updates the Quizz.max_score value.

        Args:
            filepath (str): absolute or relative path to the yaml file

        Returns:
            int:    the number of question loaded

        """
        quizz_data = load_from_file(filepath)

        if quizz_data is None:
            raise UnableToLoadQuizz

        questions = quizz_data.pop("questions")
        self.meta = quizz_data

        for q in questions:
            answers = q.pop("answers")
            self.questions.append(get_question(answers=answers, **q))

        if self.shuffle_questions:
            shuffle(self.questions)

        self.max_score = sum(question.score for question in self.questions)

        return len(self.questions)





