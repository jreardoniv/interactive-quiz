import datetime
import random

class Quiz:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.questions = []
        self.score = 0
        self.correct_count = 0
        self.total_points = 0
        self.completion_time = 0

    def print_header(self):
        return f"\n\n*******************************************\nQUIZ NAME: {self.name}\nDESCRIPTION: {self.description}\nQUESTIONS: {len(self.questions)}\nTOTAL POINTS: {self.total_points}\n*******************************************\n"

    def print_results(self, quiztaker, thefile=None):
        result_str = f"*******************************************\nRESULTS for {quiztaker}\nDate: {datetime.datetime.today()}\nTest Completion Time: {self.completion_time}\nQUESTIONS: {self.correct_count} out of {len(self.questions)} correct\nSCORE: {self.score} points of possible {self.total_points}\n*******************************************\n"
        if thefile:
            print(result_str, file=thefile, flush=True)
        else:
            return result_str

    def take_quiz(self, gui_callback):
        self.score = 0
        self.correct_count = 0
        self.completion_time = 0
        for q in self.questions:
            q.is_correct = False

        random.shuffle(self.questions)
        self.starttime = datetime.datetime.now()
        self.current_question_index = 0
        self.gui_callback = gui_callback

        self.ask_next_question()

    def ask_next_question(self):
        if self.current_question_index < len(self.questions):
            current_question = self.questions[self.current_question_index]
            self.gui_callback(current_question)
        else:
            self.endtime = datetime.datetime.now()
            self.completion_time = self.endtime - self.starttime
            self.completion_time = datetime.timedelta(seconds=round(self.completion_time.total_seconds()))
            self.gui_callback(None, finished=True)

    def answer_question(self, is_correct):
        current_question = self.questions[self.current_question_index]
        current_question.is_correct = is_correct
        if is_correct:
            self.correct_count += 1
            self.score += current_question.points

        self.current_question_index += 1
        self.ask_next_question()


class Question:
    def __init__(self):
        self.points = 0
        self.correct_answer = ""
        self.text = ""
        self.is_correct = False

class QuestionTF(Question):
    def __init__(self):
        super().__init__()

class QuestionMC(Question):
    def __init__(self):
        super().__init__()
        self.answers = []

class Answer:
    def __init__(self):
        self.text = ""
        self.name = ""