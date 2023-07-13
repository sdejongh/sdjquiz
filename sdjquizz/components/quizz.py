from sdjquizz.components.question import Answer, Question, QuestionType, get_question
from pathlib import Path
import yaml


class UnableToLoadQuizz(Exception):
    pass


def load_from_file(filepath: str) -> dict or None:
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
    def __init__(self, shuffle_questions=True, show_explanations=False):
        self.meta = {}
        self.questions = []
        self.shuffle_questions = shuffle_questions
        self.max_score = 0
        self.current_score = 0
        self.show_explanation = show_explanations

    def load(self, filepath: str) -> list[Question]:
        quizz_data = load_from_file(filepath)

        if quizz_data is None:
            raise UnableToLoadQuizz

        questions = quizz_data.pop("questions")
        self.meta = quizz_data

        for q in questions:
            answers = q.pop("answers")
            self.questions.append(get_question(answers=answers, **q))

        return self.questions





