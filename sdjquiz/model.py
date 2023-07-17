import random
import uuid
from sdjquiz.exceptions import AnswerError, QuestionError, QuizzError


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
                 unique_id: str or None = None) -> None:
        self.__unique_id = unique_id if unique_id is not None else str(uuid.uuid4())
        self.__title = title
        self.__text = text
        self.__keywords = keywords
        self.__score = score
        self.__answers = answers

    def __repr__(self):
        return f"Question(title={repr(self.title):.20}, text={repr(self.text):.20}, keywords={repr(self.keywords)}," \
               f"score={self.score}, answers={repr(self.__answers)}, unique_id={repr(self.__unique_id)})"

    def __str__(self):
        return self.text.lower()

    @property
    def unique_id(self):
        return self.__unique_id

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
        self.__score = score

    @property
    def answers(self) -> list[Answer]:
        return self.__answers

    def add_answer(self, text: str, correct: bool) -> None:
        """
        Adds an answer to the answers list
        Args:
            text (str):     the answer text
            correct (bool): True if the answer is correct

        Returns:
            None
        """
        self.__answers.append(Answer(text, correct))

    def delete_answer_by_index(self, answer_index) -> None:
        """
        Deletes an answer from the answers list based on its index.
        Raises AnswerDoesNotExistError if the index is out of range

        Args:
            answer_index (int): Index of the answer in self.__answers

        Returns:
            None
        """
        if answer_index not in range(len(self.__answers)):
            raise AnswerError(f"Cannot delete answer: index {answer_index} out of range")
        del self.__answers[answer_index]

    def update_answer(self, answer_index: int, text: str or None = None, correct: bool or None = None) -> None:
        """
        Updates an answer in the list of answers based on its index.
        Raises AnswerDoesNotExistError if the index is out of range

        Args:
            answer_index (int): the index of the answer in the answers list
            text (str): the text of the answer to be set (or None if nothing to change)
            correct (bool): the value of the answer (or None if nothing to change)

        Returns:
            None
        """
        if answer_index not in range(len(self.__answers)):
            raise AnswerError(f"Cannot update answer: index {answer_index} out of range")
        if text is not None:
            self.__answers[answer_index].text = text
        if correct is not None:
            self.__answers[answer_index].correct = correct

    def purge_answers(self) -> None:
        """
        Remove all answers from the answers list

        Returns:
            None
        """
        self.__answers.clear()

    def set_answers(self, answers: list[Answer]) -> None:
        """
        Sets or replace all answers with the given list

        Args:
            answers (list[Answer]):     list of answers

        Returns:
            None
        """
        self.__answers = answers

    def add_keywords(self, keywords: list[str]) -> None:
        """
        Adds a list of keywords tho the keywords list.
        Will only add keywords not already in the list.

        Args:
            keywords (list[str]): the list of keywords to add

        Returns:
            None
        """
        keywords = set(keyword.lower() for keyword in keywords)
        self.__keywords = sorted(list(set(self.__keywords).union(keywords)))

    def delete_keywords(self, keywords: list[str]) -> None:
        """
        Deletes a list keywords tho the keywords list.

        Args:
            keywords (list[str]): the list of keywords to remove

        Returns:
            None
        """
        keywords = set(keyword.lower() for keyword in keywords)
        self.__keywords = sorted(list(set(self.__keywords) - set(keywords)))

    def purge_keywords(self) -> None:
        """Removes all keywords"""
        self.__keywords.clear()

    def set_keywords(self, keywords: list[str]) -> None:
        """
        Sets the list of keywords. All keywords will be converted to lowercase.
        The list my contain duplicates, only one occurrence will be added to the list.

        Args:
            keywords (list[str]): the list of keywords.

        Returns:
            None
        """
        self.__keywords = sorted([keyword.lower() for keyword in set(keywords)])

    @staticmethod
    def from_dict(question_data: dict):
        """
        Returns a new Question object from the provided dictionary.

        Args:
            question_data (dict): the question data.

        Returns:
            Question: a new Question object instance.
        """
        answers = [Answer(**answer) for answer in question_data["answers"]]
        question_data['answers'] = answers
        return Question(**question_data)


class Quiz:
    """Represents a Quiz"""
    def __init__(self, title: str, author: str, description: str, questions: list[Question] or None = None) -> None:
        self.__title = title
        self.author = author
        self.__description = description
        self.__questions_bank = {question.unique_id: question for question in questions} if questions is not None else {}

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str) -> None:
        self.__title = title.lower()

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        self.__description = description.lower()

    @property
    def questions_count(self) -> int:
        if self.__questions_bank is None:
            return 0
        else:
            return len(self.__questions_bank)

    @property
    def max_score(self) -> int:
        return sum(question.score for question in self.__questions_bank.values()) if self.questions_count > 0 else 0

    def __repr__(self):
        return f"Quiz(title={repr(self.__title)}, description={repr(self.__description):.20}," \
               f"questions={repr(self.__questions_bank)}"

    def __str__(self):
        return f"{self.__title} ({self.__description})"

    @staticmethod
    def from_dict(quiz_data):
        """
        Returns a new Quiz from the provided dictionary
        Args:
            quiz_data (dict): the data of the quiz.

        Returns:
            Quiz:   A Quiz Object instance.
        """
        questions = [Question.from_dict(question_data) for question_data in quiz_data["questions"]]
        quiz_data["questions"] = questions
        try:
            quiz = Quiz(**quiz_data)
        except TypeError as error:
            raise QuizzError(error)
        except ValueError as error:
            raise QuizzError(error)
        else:
            return quiz

    def add_question(self, title: str, text: str, keywords: list[str], score: int, answers: list[Answer],
                     unique_id: str or None = None) -> None:
        """
        Adds a new question to the question bank.
        Checks unicity based on question unique_id.

        Args:
            title (str):                title of the question
            text (str):                 body of the question
            keywords (list[str]):       a list of keywords
            score (int):                value of the question
            answers: list[Answer]:      the list of answers
            unique_id: (str or None):   the question unique id

        Returns:
            None
        """
        try:
            question = Question(title, text, keywords, score, answers, unique_id)
        except TypeError:
            raise QuestionError(f"Could not create question: Wrong arguments")
        except ValueError:
            raise QuestionError(f"Could not create question: Wrong arguments")
        else:
            self.__questions_bank[question.unique_id] = question

    def delete_question(self, unique_id: str) -> None:
        """
        Deletes a question from questions bank based on its unique_id.

        Args:
            unique_id (str):           the question unique_id

        Returns:
            None
        """
        if unique_id not in self.__questions_bank:
            raise QuizzError(f"Question {unique_id} not in questions bank.")
        del(self.__questions_bank[unique_id])

    def get_questions(self, count: int) -> list[Question]:
        """
        Returns a list of questions.

        Args:
            count (int):                The number of questions to return (all questions if 1 > count > max)

        Returns:
            list[Question]              The list of questions
        """
        if count < 1 or count > self.questions_count:
            count = self.questions_count

        return random.sample(list(self.__questions_bank.values()), count)
