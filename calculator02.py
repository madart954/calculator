import os

class Manage:
    def __init__(self):
        self.user_input = ""
        self.user_example = ""
        self.user_calc_result = ""

        self.user_history = History()

    def start_example(self):
        while True:
            self.user_input = int(input(
                "Press 1 if u want enter the example\n"
                "Press 2 if u want check history\n"
                "Press 3 if u want clear history\n"
                "Press 4 if u want exit\n"
            ))
            if self.user_input == 1:
                self.user_example = input("Enter example - ")
                self.user_calc_result = Calculator(self.user_example)
                print(f"answer = {self.user_calc_result.answer}")
                self.user_history.write(self.user_example,self.user_calc_result.answer)

            elif self.user_input == 2:
                self.user_history.read()

            elif self.user_input == 3:
                self.user_history.clear()

            elif self.user_input == 4:
                break


class History:
    #работа с файлами
    def __init__(self) -> None:
        self.name_file = "History_count.txt"
        self.create_file()


    def create_file(self)-> None:
        with open(self.name_file, "a+", encoding='utf-8') as f:
            pass

    def write(self,example,answer) -> None:
        with open(self.name_file, "a+", encoding='utf-8') as f:
            f.write(f"example|{example}|, answer|{answer}|\n")

    def read(self):
        with open(self.name_file,"r",encoding="utf-8") as f:
            print(f.read())

    def clear(self):
        with open(self.name_file, "w", encoding='utf-8') as f:
            pass


class Calculator:
    def __init__(self, text):
        self.text = text
        print(self.text)
        self.token_data = list()
        self.rpn_list = list()
        self.count_list = list()
        self.answer = ""
        self.run()

    def run(self):
        self.token_data = Tokenizer(self.text)
        try:
            self.token_data.run()
            print("Data_tokenizer",self.token_data.data_tokenizer)
        except Tokenizer_error as e:
            print(f"Ошибка {e}")
            return print("ошибка в токенизации ")

        self.rpn_list = RPN(self.token_data.data_tokenizer)
        self.rpn_list.run()
        print("Queue",self.rpn_list.queue)

        self.count_list = Count(self.rpn_list.queue)
        self.count_list.run()
        self.answer = self.count_list.stack[-1]
        print(self.answer)

        #не работает
        return self.answer


class Tokenizer:
    def __init__(self, text):
        self.data_tokenizer = list()
        self.text_token = text
        self.buffer = ""
        self.state = "START"
        self.handlers = {
            "START": self.start_token,
            "NUMBER": self.numb_token,
            "FLOAT": self.float_token,
            "OP": self.op_token,
            "ERROR": self.error
        }

    #управвлящая функция
    def run(self):
        ch: str
        for ch in self.text_token:
            # функции в словаре (состояние как индекс (элемент записи))
            self.handlers[self.state](ch)
        else:
            if self.buffer:
                self.data_tokenizer.append(self.buffer)

    #машина состояний
    def start_token(self, ch: str):
        if ch.isdigit():
            self.add_to_buffer(ch, "NUMBER")
        elif ch in "+-(":
            self.data_tokenizer.append(ch)
            self.state = "OP"
        else:
            self.error(ch)

    def numb_token(self, ch: str):

        if ch.isdigit():
            self.add_to_buffer(ch, "NUMBER")
        elif ch in "+-/*":
            self.clearing_buffer(ch, "OP")
        elif ch in "()":
            if ch == "(":
                self.error(ch)
            elif ch == ")":
                self.clearing_buffer(ch, "OP")
        elif ch == ".":
            self.add_to_buffer(ch, "FLOAT")
        else:
            self.error(ch)

    def float_token(self, ch: str):
        if ch.isdigit():
            self.add_to_buffer(ch, "FLOAT")
        elif ch == ".":
            self.error(ch)
        elif ch in ")" and self.buffer[-1] == ".":
            self.clearing_buffer(ch, "OP")
        elif ch in ")" and self.buffer[-1].isdigit():
             self.clearing_buffer(ch,"OP")
        elif ch in "+-*/" and self.buffer[-1] != ".":
            self.clearing_buffer(ch, "OP")
        else:
            self.error(ch)

    def op_token(self, ch: str):
        if ch.isdigit():
            self.add_to_buffer(ch, "NUMBER")
        elif ch in "+-*/" and self.data_tokenizer[-1] not in "+-/*":
            self.clearing_buffer(ch, "OP")
        elif ch == "(":
            self.clearing_buffer(ch, "OP")
        else:
            self.error(ch)

    #вспомогательные функции
    def add_to_buffer(self, ch, new_state):
        self.buffer += ch
        self.state = new_state

    def clearing_buffer(self, ch, new_state):
        if self.buffer != "":
            self.data_tokenizer.append(self.buffer)
            self.buffer = ""
        self.data_tokenizer.append(ch)
        self.state = new_state

    def error(self,ch:str = ""):
        raise Tokenizer_error(f"Неверный символ '{ch}' в состоянии {self.state}")


class RPN:
    def __init__(self,data_list_tokens):
        self.data_list_tokens = data_list_tokens
        self.stack = list()
        self.queue = list()
        self.element_priority = {
            "+-": 1,
            "*/": 2,
            "~": 3
        }

    def run(self):
        #унарный минус
        #базовое выталкивание до скобок
        #обработка скобок
        """Перебираем значенине токенизатора"""
        flag = False
        for index, element_token in enumerate(self.data_list_tokens):
            if flag:
                break

            # print(f"primer {self.data_list_tokens}\n"
            #       f"element_token = '{element_token}' and index = '{index}'\n"
            #       f"stack = '{self.stack}'\n"
            #       f"queue = '{self.queue}'\n"
            #       f"element_token -1 = '{self.data_list_tokens[index-1]}'\n ")
            #унарный минус первого вхождение
            if index == 0 and element_token == "-":
                self.stack.append("~")
            #число
            elif is_number(element_token):
                self.queue.append(element_token)
            #если пустой
            elif not self.stack:
                self.stack.append(element_token)

            # обработка скобок
            elif element_token in "()":
                if element_token == "(":
                    self.stack.append(element_token)
                else:
                    while True:
                        ch = self.stack.pop()
                        if ch != "(":
                            self.queue.append(ch)
                        else:
                            break

            #обработка минусов
            elif element_token == "-":
                #бинарный минус перед скобкой ) или числом
                if (self.data_list_tokens[index - 1] == ")"
                        or is_number(self.data_list_tokens[index - 1])):
                    self.input_queue_ch(element_token)
                # унарный минус после скобки ( и перед знаком
                elif (self.data_list_tokens[index - 1] == "("
                      or not is_number(self.data_list_tokens[index - 1])):
                    self.input_queue_ch("~")
            #остальные знаки
            elif not is_number(element_token):
                self.input_queue_ch(element_token)

            else:
                self.error(ch)
                break
        #остальной стэк
        else:
            self.queue.extend(reversed(self.stack) )

    def input_queue_ch(self,ch_stack):
        """ помещеаем элемент в очередь или стэк сравнивая их приоритет
        Пока верхушка стэка >= приходящего элемента из токенов => выталкиваем
        иначе прибавляем просто в стэк"""

        #print(f"stack priority = {self.chek_priority(self.stack[-1])}\n "
              #f"element priority = {self.chek_priority(ch_stack)}\n ")
        #если в стэк последняя скобка просто добавляем элемент
        if self.stack[-1] in "()":
            self.stack.append(ch_stack)
        else:
            while self.chek_priority(self.stack[-1]) >= self.chek_priority(ch_stack):
                element_stack = self.stack.pop()
                self.queue.append(element_stack)
                try:
                    #если в стэке останавливаемся на скобке просто добавляем элемент
                    if self.stack[-1] == "(":
                        self.stack.append(ch_stack)
                        break
                except IndexError:
                    #если стэк пустой
                    self.stack.append(ch_stack)
                    break
            else:
                self.stack.append(ch_stack)

    def chek_priority(self,ch):
        for key in self.element_priority:
            if ch in key:
                return self.element_priority[key]
        return None

    def error(self):
        print("error RPN")


class Count:
    def __init__(self,rpn_list):
        self.rpn_queue = rpn_list
        self.stack = list()
        self.temp_count = None

    def run(self)-> None:
        char:str
        for char in self.rpn_queue:
            # print(f"sign = {char} ")
            # print(f"stack_count = {self.stack}\n")
            if  is_number(char) :
                self.stack.append(char)
            else:
                if char == "~":
                    self.stack[-1] = "-" + self.stack[-1]
                else:
                    element_count1 = self.stack.pop(-2)
                    element_count2 = self.stack.pop(-1)
                    temp_count = self.operation_math(element_count1, element_count2, char)
                    self.stack.append(temp_count)

    def operation_math( self, el1:str, el2:str, sign_op:str) -> str:
        numb1 = float(el1)
        numb2 = float(el2)
        operator = sign_op
        operation = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y
        }
        return str(operation[operator](numb1, numb2))

 # STATIC def
def is_number(element):
        try:
            float(element)
            return True
        except ValueError:
            return False

#Errors
class Tokenizer_error(Exception):
    pass

if __name__ == "__main__":
    # x = Calculator("-13.3+(-31.2)*0.1").answer
    y = Calculator("2++3").answer
    print(y)

    # start = Manage()
    # start.start_example()
