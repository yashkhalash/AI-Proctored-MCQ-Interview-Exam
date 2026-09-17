import json
from pathlib import Path

class ExamEngine:
    def __init__(self):
        self.questions = json.loads(Path("questions.json").read_text())
        self.index = 0
        self.answers = []
        self.finished = False

    def current_question(self):
        if self.finished or self.index >= len(self.questions):
            return None
        return self.questions[self.index]

    def answer(self, selected):
        q = self.current_question()
        if not q:
            return
        self.answers.append({
            "question": q["question"],
            "selected": selected,
            "correct": selected == q["answer"]
        })
        self.index += 1
        if self.index >= len(self.questions):
            self.finished = True

    def result(self):
        correct = sum(x["correct"] for x in self.answers)
        total = len(self.questions)
        return {
            "score": correct,
            "total": total,
            "percentage": round(correct / total * 100, 2) if total else 0,
            "answers": self.answers
        }
