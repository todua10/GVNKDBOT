import vk_api, cfg
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
from vk_api import VkUpload
attachments = []
photos = {}

vk_session = vk_api.VkApi(token=cfg.access_token2)
upload = VkUpload(vk_session)


image = "C:/Users/dontn/Desktop/_9hHVG3Loc8.jpg"
upload_image = upload.photo_messages(photos=image)[0]


# Класс ответа от бота. Нужен для того, чтобы бот мог задавать вопросы с выбором ответа и отправлять клавиатуру
class Answer:
    def __init__(self, text="Ошибка", answers=None, one_time=True, inline=False, keyboard=None, attachments=None):
        self.text = text
        self.answers = answers
        self.one_time = one_time
        self.inline = inline
        self.keyboard = keyboard
        self.attachments = attachments


class Bot:
    def __init__(self, user_id):
        self._user_id = user_id
        self.welcome_message_sent = False
        self.next_task = "talk" # Переменная необходимая, чтобы переключать режим работы бота
        self.last_quesion = -1 # Переменная для прохождения теста
        self.possible_answers = None # Ответы на текцщий вопрос
        self.last_keyboard = None # Хранение клавиатуры на случай неправильного ввода ответа


# Вызывает функцию для текущей задачи. Нужно для того, чтобы можно было обращаться к одной функции
    def update(self, text):

        if self.next_task == "talk":
            return self.talk(text)

        if self.next_task == "main_menu":
            return self.main_menu()

        if self.next_task == "test":
            return self.test(text)

        if self.next_task == "show_meme":
            return self.show_meme(text)

        if self.next_task == "show_user_stat":
            return self.show_user_stat(text)

        if self.next_task == "show_all_stat":
            return self.show_all_stat(text)

        if self.next_task == "upload_meme":
            return self.upload_meme(text)


# Здесь бот принимает сообщения и определяет дальнейшую работу
    def talk(self, text):
        if text.lower() in ("привет", "ку", "здарвствуйте", "вернуться в начало", "начало"):
            return self.main_menu()

        elif text.lower() in ("help", "помощь", "команды"):
            return self.help()

        elif text.lower() in ("начать тест", "тест", "вопросы"):
            return self.test("$")

        elif text.lower() in ("показать мем", "хочу мем", "мем"):
            return self.show_meme(text)

        elif text.lower() in ("статистика", "показать статистику", "личная статистика"):
            return self.show_stat("$")

        elif text.lower() in ("загрузить мем", "загрузить фото"):
            return self.upload_meme(text)

        else:
            return Answer("Команда не распознана")


# Функции бота
    def main_menu(self):
        self.next_task = "talk"
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("Начать тест", color=VkKeyboardColor.POSITIVE)
        keyboard.add_button("Мем", color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button("Статистика", color=VkKeyboardColor.PRIMARY)
        keyboard.add_button("Загрузить мем", color=VkKeyboardColor.SECONDARY)
        if not self.welcome_message_sent:
            self.welcome_message_sent = True
            return Answer("Привет вездекодерам!", keyboard=keyboard)
        else:
            return Answer("Главное меню", keyboard=keyboard)


    def help(self):
        return Answer("Список доступных команд:\n\n"
                      "начать тест\n"
                      "показать мем\n"
                      "статистика\n"
                      "загрузить мем\n"
                      "вернуться в начало | начало")


    def test(self, text):
        self.next_task = "test"
        questions = (("Как настроение?", "Отлично",  "Не очень"),
                     ("Вопрос 2", "ответ 1", "ответ 2", "ответ 3"),
                     ("Где ты живешь?", "место"),
                     ("Вопрос 4", "Положительно", "Нейтрально", "Отрицательно"),
                     ("Вопрос 5", "ответ 1", "ответ 2", "ответ 3", "ответ 4"),
                     ("Вопрос 6", "ответ 1", "ответ 2"),
                     ("Вопрос 7", "ответ 1", "ответ 2", "ответ 3"),
                     ("Вопрос 8", "ответ 1", "ответ 2", "ответ 3"))
        ans = Answer()

        if text == "$": # $ - символ для начала теста
            self.last_quesion += 1
            self.possible_answers = questions[self.last_quesion][1:]

            keyboard = VkKeyboard(inline=True)
            keyboard.add_button(questions[self.last_quesion][1], color=VkKeyboardColor.POSITIVE)
            keyboard.add_button(questions[0][2], color=VkKeyboardColor.NEGATIVE)
            self.last_keyboard = keyboard

            return Answer(questions[0][0], keyboard=keyboard)

        elif text in self.possible_answers and self.last_quesion == 0:
            self.last_quesion += 1
            self.possible_answers = questions[self.last_quesion][1:]

            keyboard = VkKeyboard(inline=True)
            keyboard.add_button(questions[self.last_quesion][1], color=VkKeyboardColor.POSITIVE)
            keyboard.add_button(questions[self.last_quesion][2], color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button(questions[self.last_quesion][3], color=VkKeyboardColor.NEGATIVE)
            self.last_keyboard = keyboard

            return Answer(questions[self.last_quesion][0], keyboard=keyboard)

        elif text in self.possible_answers and self.last_quesion == 1:
            self.last_quesion += 1
            self.possible_answers = questions[self.last_quesion][1:]

            keyboard = VkKeyboard(inline=True)
            # кнопка на локации, можно доработать
            keyboard.add_location_button()
            self.last_keyboard = keyboard

            return Answer(questions[self.last_quesion][0], keyboard=keyboard)

        # здесь нет проверки на ответ
        elif not text and self.last_quesion == 2:
            self.last_quesion += 1
            self.possible_answers = questions[self.last_quesion][1:]

            keyboard = VkKeyboard(inline=True)
            keyboard.add_button(questions[self.last_quesion][1], color=VkKeyboardColor.POSITIVE)
            keyboard.add_button(questions[self.last_quesion][2], color=VkKeyboardColor.PRIMARY)
            keyboard.add_button(questions[self.last_quesion][3], color=VkKeyboardColor.NEGATIVE)
            self.last_keyboard = keyboard

            return Answer(questions[self.last_quesion][0], keyboard=keyboard)

        elif text in self.possible_answers and self.last_quesion == 3:
            self.last_quesion += 1
            self.possible_answers = questions[self.last_quesion][1:]

            keyboard = VkKeyboard(inline=True)
            keyboard.add_button(questions[self.last_quesion][1], color=VkKeyboardColor.POSITIVE)
            keyboard.add_button(questions[self.last_quesion][2], color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button(questions[self.last_quesion][3], color=VkKeyboardColor.POSITIVE)
            keyboard.add_button(questions[self.last_quesion][4], color=VkKeyboardColor.NEGATIVE)
            self.last_keyboard = keyboard

            return Answer(questions[self.last_quesion][0], keyboard=keyboard)

        elif text in self.possible_answers and self.last_quesion == 4:
            self.last_quesion += 1
            self.possible_answers = questions[self.last_quesion][1:]

            keyboard = VkKeyboard(inline=True)
            keyboard.add_button(questions[self.last_quesion][1], color=VkKeyboardColor.POSITIVE)
            keyboard.add_button(questions[self.last_quesion][2], color=VkKeyboardColor.NEGATIVE)
            self.last_keyboard = keyboard

            return Answer(questions[self.last_quesion][0], keyboard=keyboard)

        elif text in self.possible_answers and self.last_quesion == 5:
            self.last_quesion += 1
            self.possible_answers = questions[self.last_quesion][1:]

            keyboard = VkKeyboard(inline=True)
            keyboard.add_button(questions[self.last_quesion][1], color=VkKeyboardColor.POSITIVE)
            keyboard.add_button(questions[self.last_quesion][2], color=VkKeyboardColor.PRIMARY)
            keyboard.add_button(questions[self.last_quesion][2], color=VkKeyboardColor.NEGATIVE)
            self.last_keyboard = keyboard

            return Answer(questions[self.last_quesion][0], keyboard=keyboard)

        elif text in self.possible_answers and self.last_quesion == 6:
            self.last_quesion += 1
            self.possible_answers = questions[self.last_quesion][1:]

            keyboard = VkKeyboard(inline=True)
            keyboard.add_button(questions[self.last_quesion][1], color=VkKeyboardColor.POSITIVE)
            keyboard.add_button(questions[self.last_quesion][2], color=VkKeyboardColor.PRIMARY)
            keyboard.add_button(questions[self.last_quesion][2], color=VkKeyboardColor.NEGATIVE)
            self.last_keyboard = keyboard

            return Answer(questions[self.last_quesion][0], keyboard=keyboard)

        elif text in self.possible_answers or text in ("вернуться в начало", "начало", "закончить"):
            self.possible_answers = None
            self.last_quesion = -1
            self.next_task = "main_menu"
            return self.main_menu()

        else:
            print(text)
            return Answer("Такого ответа нет")


    def show_meme(self, text):
        self.next_task = "show_meme"
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button("Лайк", color=VkKeyboardColor.POSITIVE)
        keyboard.add_button("Дизлайк", color=VkKeyboardColor.NEGATIVE)

        image = "C:/Users/dontn/Desktop/_9hHVG3Loc8.jpg"
        upload_image = upload.photo_messages(photos=image)[0]
        attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
        return Answer("text", keyboard=keyboard, attachments=','.join(attachments))


    def show_stat(self, text):
        #self.next_task = "show_stat"
        return Answer("Функция пока не доступна")


    def upload_meme(self, text):
        #self.next_task = "upload_meme"
        return Answer("Функция пока не доступна")
