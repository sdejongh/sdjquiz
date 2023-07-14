from sdjquiz.controller import QuizController
from sdjquiz.vue import QuizTUI


def main():
    controller = QuizController(QuizTUI())
    controller.start()


if __name__ == "__main__":
    main()
