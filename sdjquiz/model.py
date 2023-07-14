import uuid
from sdjquiz.exceptions import AnswerError


class Answer:
    """Represents an answer of a question"""
    def __init__(self, text: str, correct: bool = False) -> None:
        self.text = text
        self.correct = correct

    def __repr__(self) -> str:
        return f"Answer(text='{self.text:.30}', correct={self.correct})"

    def __str__(self) -> str:
        return self.text.lower()


class Question:
    """Represents a multiple choice question"""
    def __init__(self, title: str, text: str, keywords: list[str], score: int, answers: list[Answer],
                 question_uuid: str or None = None) -> None:
        self.uuid = question_uuid if question_uuid is not None else str(uuid.uuid4())
        self.__title = title
        self.__text = text
        self.__keywords = keywords
        self.__score = score
        self.__answers = answers

    def __repr__(self):
        return f"Question(title={repr(self.title):.20}, text={repr(self.text):.20}, keywords={repr(self.keywords)}," \
               f"score={self.score}, answers={repr(self.__answers)}, uuid={repr(self.uuid)})"

    def __str__(self):
        return self.text.lower()

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, text: str):
        self.__title = text.lower()

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text.lower()

    @property
    def keywords(self):
        return self.__keywords

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, score) -> None:
        if score < 0:
            raise ValueError(f"Score value {score} is incorrect. Must be >= 0")

    def add_answer(self, text: str, correct: bool) -> None:
        """Adds an answer to the answers list"""
        self.__answers.append(Answer(text, correct))

    def delete_answer_by_index(self, answer_index) -> None:
        """Deletes an answer from the answers list based on its index.
        Raises AnswerDoesNotExistError if the index is out of range

        Args:
            answer_index (int): Index of the answer in self.__answers

        Returns:

        """
        if answer_index not in range(len(self.__answers)):
            raise AnswerError(f"Cannot delete answer: index {answer_index} out of range")
        del self.__answers[answer_index]

    def update_answer(self, answer_index: int, text: str or None = None, correct: bool or None = None) -> None:
        """Updates an answer in the list of answers based on its index.
        Raises AnswerDoesNotExistError if the index is out of range

        Args:
            answer_index (int): the index of the answer in the answers list
            text (str): the text of the answer to be set (or None if nothing to change)
            correct (bool): the value of the answer (or None if nothing to change)

        Returns:

        """
        if answer_index not in range(len(self.__answers)):
            raise AnswerError(f"Cannot update answer: index {answer_index} out of range")
        if text is not None:
            self.__answers[answer_index].text = text
        if correct is not None:
            self.__answers[answer_index].correct = correct

    def purge_answers(self) -> None:
        """Remove all answers from the answers list"""
        self.__answers.clear()

    def set_answers(self, answers: list[Answer]) -> None:
        """Sets or replace all answers with the given list"""
        self.__answers = answers

    def add_keywords(self, keywords: list[str]) -> None:
        """Adds a list of keywords tho the keywords list.
        Will only add keywords not already in the list.

        Args:
            keywords (list[str]): the list of keywords to add

        Returns:

        """
        keywords = set(keyword.lower() for keyword in keywords)
        self.__keywords = sorted(list(set(self.__keywords).union(keywords)))

    def delete_keywords(self, keywords: list[str]) -> None:
        """Deletes a list keywords tho the keywords list.

        Args:
            keywords (list[str]): the list of keywords to remove

        Returns:

        """
        keywords = set(keyword.lower() for keyword in keywords)
        self.__keywords = sorted(list(set(self.__keywords) - set(keywords)))

    def purge_keywords(self) -> None:
        """Removes all keywords"""
        self.__keywords.clear()

    def set_keywords(self, keywords: list[str]) -> None:
        """Sets the list of keywords. All keywords will be converted to lowercase.
        The list my contain duplicates, only one occurrence will be added to the list.

        Args:
            keywords (list[str]): the list of keywords.

        Returns:

        """
        self.__keywords = sorted([keyword.lower() for keyword in set(keywords)])


class Quiz:
    """Represents a Quiz"""
    def __init__(self, title: str, description: str, questions: list[Question] or None = None) -> None:
        self.title = title
        self.description = description
        self.questions_bank = {question.uuid: question for question in questions}
        self.max_score = sum(question.score for question in self.questions_bank)

    @property
    def questions_count(self):
        """Returns the number of questions in the quiz"""
        return len(self.questions_bank)

    def __repr__(self):
        return f"Quiz(title={repr(self.title)}, description={repr(self.description):.20}," \
               f"questions={repr(self.questions_bank)}"

    def __str__(self):
        return f"{self.title.lower()} ({self.description.lower()})"
