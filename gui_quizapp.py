import tkinter as tk
from tkinter import messagebox
from quizmanager import QuizManager
from quiz import QuestionMC, QuestionTF
import os
import datetime


class QuizApp:
    QUIZ_FOLDER = "Quizzes"

    def __init__(self, root):
        self.root = root
        self.root.title("Movie Trivia")
        self.username = ""
        self.result = None
        self.qm = QuizManager(QuizApp.QUIZ_FOLDER)
        self.create_widgets()

    def create_widgets(self):
        self.header_label = tk.Label(self.root, text="Welcome to Movie Trivia!", font=("Helvetica", 16))
        self.header_label.pack(pady=10)

        self.username_label = tk.Label(self.root, text="Please enter your name:")
        self.username_label.pack(pady=5)
        
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Start Quiz", command=self.start_quiz)
        self.start_button.pack(pady=10)

        self.results_button = tk.Button(self.root, text="Show Results", command=self.show_results, state=tk.DISABLED)
        self.results_button.pack(pady=5)

    def start_quiz(self):
        self.username = self.username_entry.get()
        if not self.username:
            messagebox.showerror("Error", "Please enter your name to start the quiz.")
            return
        
        self.quiz_selection_window = tk.Toplevel(self.root)
        self.quiz_selection_window.title("Select a Quiz")
        self.quiz_selection_window.geometry("400x300")

        self.quiz_label = tk.Label(self.quiz_selection_window, text="Select a Quiz:")
        self.quiz_label.pack(pady=5)

        self.quiz_listbox = tk.Listbox(self.quiz_selection_window)
        self.quiz_listbox.pack(pady=5)

        for quiz_id, quiz in self.qm.quizzes.items():
            self.quiz_listbox.insert(tk.END, f"{quiz_id}. {quiz.name}")

        self.select_button = tk.Button(self.quiz_selection_window, text="Select", command=self.select_quiz)
        self.select_button.pack(pady=5)

    def select_quiz(self):
        selected = self.quiz_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a quiz.")
            return
        
        quiz_id = int(self.quiz_listbox.get(selected).split(".")[0])
        self.qm.the_quiz = self.qm.quizzes[quiz_id]

        self.quiz_selection_window.destroy()

        self.quiz_window = tk.Toplevel(self.root)
        self.quiz_window.title("Quiz Time")
        self.quiz_window.geometry("400x300")

        self.question_label = tk.Label(self.quiz_window, text="", wraplength=380)
        self.question_label.pack(pady=10)

        self.answer_frame = tk.Frame(self.quiz_window)
        self.answer_frame.pack(pady=10)

        self.next_button = tk.Button(self.quiz_window, text="Next", command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(pady=10)

        self.current_question = None
        self.current_question_var = tk.StringVar()

        self.qm.the_quiz.take_quiz(self.show_question)

    def show_question(self, question, finished=False):
        if finished:
            if self.quiz_window is not None:
                self.quiz_window.destroy()
                self.quiz_window = None  # Avoid referencing a destroyed window
            self.results_button.config(state=tk.NORMAL)
            messagebox.showinfo("Quiz Completed", f"Quiz completed!\nScore: {self.qm.the_quiz.score}/{self.qm.the_quiz.total_points}\nCorrect Answers: {self.qm.the_quiz.correct_count}/{len(self.qm.the_quiz.questions)}")
            return

        self.current_question = question
        self.question_label.config(text=question.text)
        self.current_question_var.set("")

        for widget in self.answer_frame.winfo_children():
            widget.destroy()

        if isinstance(question, QuestionTF):
            tk.Radiobutton(self.answer_frame, text="True", variable=self.current_question_var, value="t", command=self.enable_next).pack(anchor=tk.W)
            tk.Radiobutton(self.answer_frame, text="False", variable=self.current_question_var, value="f", command=self.enable_next).pack(anchor=tk.W)
        elif isinstance(question, QuestionMC):
            for answer in question.answers:
                tk.Radiobutton(self.answer_frame, text=answer.text, variable=self.current_question_var, value=answer.name, command=self.enable_next).pack(anchor=tk.W)

    def enable_next(self):
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        try:
            is_correct = self.current_question_var.get() == self.current_question.correct_answer
            self.qm.the_quiz.answer_question(is_correct)
            if self.next_button.winfo_exists():
                self.next_button.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error in next_question: {e}")

    def show_results(self):
        results_window = tk.Toplevel(self.root)
        results_window.title("Quiz Results")
        results_window.geometry("400x300")

        results_text = tk.Text(results_window, wrap=tk.WORD)
        results_text.pack(expand=True, fill=tk.BOTH)

        results = self.qm.the_quiz.print_results(self.username, thefile=None)
        results_text.insert(tk.END, results)

        save_button = tk.Button(results_window, text="Save Results", command=self.save_results)
        save_button.pack(pady=10)

    def save_results(self):
        today = datetime.datetime.now()
        filename = f"QuizResults_{today.year}_{today.month}_{today.day}.txt"
        n = 1
        while os.path.exists(filename):
            filename = f"QuizResults_{today.year}_{today.month}_{today.day}_{n}.txt"
            n += 1

        with open(filename, "w") as f:
            self.qm.the_quiz.print_results(self.username, f)

        messagebox.showinfo("Results Saved", "Quiz results have been saved!")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()