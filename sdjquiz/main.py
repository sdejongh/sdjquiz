from sdjquiz.controller import ConsoleQuizController
import signal
import sys


def signal_handler(sig, frame):
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    controller = ConsoleQuizController()
    controller.start()


if __name__ == "__main__":
    main()
