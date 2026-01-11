import random
from script import common

class ScienceQuestionCreator():
    def __init__(self):
        self.difficulty = common.get_settings("difficulty")
        self.allQuestions = common.get_subject_json("science")
    
    def main(self):
        questions_list = self.get_questions()
        
        if not questions_list:
            return {
                "question": "もんだいがありません",
                "answer": "",
                "choices": []
            }
            
        target_q = self.select_question(questions_list)
        return target_q

    def get_questions(self):
        self.difficulty = common.get_settings("difficulty") 
        key = f"grade{self.difficulty}"
        
        if self.allQuestions and key in self.allQuestions:
            QUESTIONS = self.allQuestions[key]
        elif self.allQuestions and "grade1" in self.allQuestions:
             QUESTIONS = self.allQuestions["grade1"]
        else:
            QUESTIONS = []
        
        return QUESTIONS
    
    def select_question(self, questions_list):
        return random.choice(questions_list)
