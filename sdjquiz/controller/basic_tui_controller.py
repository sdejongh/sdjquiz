import re
from sdjquiz.controller.abstract_controller import QuizController
from sdjquiz.vue.basic_tui_vue import QuizTUI


class ConsoleQuizController(QuizController):

    def get_quiz_controller_vue(self) -> QuizTUI:
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
