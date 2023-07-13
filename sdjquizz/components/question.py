from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, asdict
from enum import Enum, auto


class QuestionType(Enum):
    SINGLE = "single"
    MULTI = "multi"


@dataclass
class Answer:
    text: str
    valid: bool


def get_question(**kwargs):
    question_type = QuestionType(kwargs.pop("type"))

    if question_type == QuestionType.SINGLE:
        return SingleChoiceQuestion(**kwargs)

    if question_type == QuestionType.MULTI:
        return MultipleChoiceQuestion(**kwargs)

    return None


class Question(ABC):
    """Abstract Question class

    Attributes:
        title (str): The question title
        text (str): The body of the question
        answers (list[Answer]): A list of all answers
        keywords (list[str]): A list of textual keywords
        score (int): the score value of the question
        type (QuestionType): the type of the question
    """
    def __init__(self, title: str, text: str, answers: list[Answer], keywords: list[str], score: int):
        self.title = title
        self.text = text
        self.answers = answers
        self.keywords = keywords
        self.score = score
        self.type = None

    def to_dict(self, randomize: bool = True) -> dict:
        """Returns a dictionary including all the question attributes.

        Args:
            randomize (bool): Randomize answers orders if True

        Returns:
            dict: The question fields as a dictionary
        """
        return {
            "title": self.title,
            "text": self.text,
            "keywords": self.keywords,
            "score": self.score,
            "type": self.type,
            "answers": [asdict(answer) for answer in self.answers],
            "valid": [idx for idx, answer in enumerate(self.answers) if answer.valid]
        }


class SingleChoiceQuestion(Question):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = QuestionType.SINGLE


class MultipleChoiceQuestion(Question):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = QuestionType.MULTI