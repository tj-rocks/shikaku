import random
from script import common

class calcCreator():
    def __init__(self, kind_flg=None):
        self.difficulty = common.get_settings("difficulty")
        self.kind_flg = kind_flg
        self.kind = "+"
        self.fst_num = 10
        self.scd_num = 10
        self.trd_num = 10
        self.formula_kind = "+"
        self.ans_num = 0
        self.formula_str = ""
        self.shikaku_value = 0

    def main(self):
        self.set_formuila_kind()
        self.set_formula_values()
        self.create_base_question()
        return self.create_shikaku_question()

    def set_formula_values(self):
        # 難易度に応じた基準値を設定
        std_value = 10
        ini_value = 1
        
        if self.difficulty <= 2:
            #足し算と引き算だけ
            std_value = 10
            ini_value = 1
        elif self.difficulty <= 4:
            #足し算と引き算は2桁　
            #掛け算は1桁
            #割り算も1桁
            if self.kind == "/" or self.kind == "*":
                std_value = 10
                ini_value = 1
            else:
                std_value = 100
                ini_value = 2
        elif self.difficulty <= 6:
            #足し算引き算は3桁
            #掛け算は2桁 
            #割り算も2桁 
            if self.kind == "/" or self.kind == "*":
                std_value = 100
                ini_value = 5
            else:
                std_value = 1000
                ini_value = 100
    
        self.fst_num = random.randint(ini_value, std_value)
        self.scd_num = random.randint(ini_value, int(std_value*0.8) + 1)
        self.trd_num = random.randint(ini_value, int(std_value*0.6) + 1)

    def set_formuila_kind(self):
        if self.difficulty <= 2:
            a = random.randint(0,1)
        elif self.difficulty <= 4:
            a = random.randint(0,2)
        elif self.difficulty <= 6:
            a = random.randint(0,3)
        else:
            a = random.randint(0,3)

        if a == 0:
            self.formula_kind = "+"
        elif a == 1:
            self.formula_kind = "-"
        elif a == 2:
            self.formula_kind = "*"
        elif a == 3:
            self.formula_kind = "/"
        
        return self.formula_kind
    
    def create_base_question(self):
        is_three_num_flg = False

        a = random.randint(0,10)
        if a < 2:
            is_three_num_flg = True
        else:
            self.trd_num = None
            is_three_num_flg = False
        
        if is_three_num_flg == False:
            if self.formula_kind == "+":
                self.ans_num = self.fst_num + self.scd_num
            elif self.formula_kind == "-":
                self.fst_num = self.adjust_num_for_subtraction(self.fst_num, self.scd_num)
                self.ans_num = self.fst_num - self.scd_num
            elif self.formula_kind == "*":
                self.ans_num = self.fst_num * self.scd_num
            elif self.formula_kind == "/":
                self.scd_num = self.adjust_num_for_deviation(self.fst_num, self.scd_num)
                self.ans_num = int(self.fst_num / self.scd_num)

        elif is_three_num_flg == True:
            if self.formula_kind == "+":
                self.ans_num = self.fst_num + self.scd_num + self.trd_num
            elif self.formula_kind == "-":
                self.fst_num = self.adjust_num_for_subtraction(self.fst_num, self.scd_num + self.trd_num)
                self.ans_num = self.fst_num - self.scd_num - self.trd_num
            elif self.formula_kind == "*":
                self.ans_num = self.fst_num * self.scd_num * self.trd_num
            elif self.formula_kind == "/":
                self.scd_num = self.adjust_num_for_deviation(self.fst_num, self.scd_num)
                temp_ans = int(self.fst_num / self.scd_num)
                self.trd_num = self.adjust_num_for_deviation(temp_ans, self.trd_num)
                self.ans_num = int(temp_ans / self.trd_num)

    def create_shikaku_question(self):
        shikaku_form = "□"

        formula_japanese_map = {
            "+": "＋",
            "-": "－",
            "*": "×",
            "/": "÷"
        }

        fst_num = self.fst_num
        scd_num = self.scd_num
        trd_num = self.trd_num
        
        if self.trd_num is None:
            a = random.randint(0,1)
            if a == 0:
                fst_num = shikaku_form
                shikaku_value = self.fst_num
            else:
                scd_num = shikaku_form
                shikaku_value = self.scd_num
            formula_str = f"{fst_num} {formula_japanese_map[self.formula_kind]} {scd_num} = {self.ans_num}"
        else:
            a = random.randint(0,2)
            if a == 0:
                fst_num = shikaku_form
                shikaku_value = self.fst_num
            elif a == 1:
                scd_num = shikaku_form
                shikaku_value = self.scd_num
            elif a == 2:
                trd_num = shikaku_form
                shikaku_value = self.trd_num
            formula_str = f"{fst_num} {formula_japanese_map[self.formula_kind]} {scd_num} {formula_japanese_map[self.formula_kind]} {trd_num} = {self.ans_num}"
        
        self.formula_str = formula_str
        self.shikaku_value = shikaku_value

        return {"formula_str": formula_str, "shikaku_value": shikaku_value}

    def adjust_num_for_subtraction(self, num01, num02):
        while num01 - num02 < 0:
            num01 += 1
        return num01

    def adjust_num_for_deviation(self, num01, num02):
        if num02 == 0: num02 = 1 
        while num01 % num02 != 0:
            num02 -= 1
            if num02 == 0: 
                num02 = 1
                break
        return num02

class wordQuestionCreator():
    def __init__(self):
        self.difficulty = common.get_settings("difficulty")
        self.allQuestions = common.get_subject_json("math")
    
    def main(self):
        questions_list = self.get_questions()
        
        if not questions_list:
            return {"formula_str": "もんだいがありません", "shikaku_value": 0}
            
        target_q = random.choice(questions_list)
        
        return {
            "formula_str": target_q["question"],
            "shikaku_value": int(target_q["answer"])
        }

    def get_questions(self):
        key = f"grade{self.difficulty}"
        
        if key in self.allQuestions:
            QUESTIONS = self.allQuestions[key]
        else:
            QUESTIONS = self.allQuestions["grade1"]
        
        return QUESTIONS
    
    def select_question(self, questions_list):
        target_q = random.choice(questions_list)
        
        return target_q
