import vk_api, cfg
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton


# Класс ответа от бота. Нужен для того, чтобы бот мог задавать вопросы с выбором ответа и отправлять клавиатуру
class Answer:
    def __init__(self, text, answers=None, one_time=True, inline=False, keyboard=None):
        self.text = text
        self.answers = answers
        self.one_time = one_time
        self.inline = inline
        self.keyboard = keyboard


class Bot:
    def __init__(self, user_id):
        self._user_id = user_id
        self.welcome_message_sent = False
        self.next_task = "talk" # Переменная необходимая, чтобы переключать режим работы бота
        self.current_quesion = 0

    # Вызывает функцию для текущей задачи. Нужно для того, чтобы можно было обращаться к одной функции
    def update(self, text):
        # Передается входное значение в функцию
        if self.next_task == "talk":
            return self.talk(text)

        if self.next_task == "welcome":
            return self.welcome()

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
            return self.welcome()

        elif text.lower() in ("help", "помощь", "команды"):
            return self.help()

        elif text.lower() in ("начать тест", "тест", "вопросы"):
            return self.test(text)

        elif text.lower() in ("показать мем", "хочу мем", "мем"):
            return self.show_meme(text)

        elif text.lower() in ("статистика", "показать статистику", "личная статистика"):
            return self.show_stat(text)

        elif text.lower() in ("загрузить мем", "загрузить фото"):
            return self.upload_meme(text)

        else:
            return Answer("Команда не распознана")


    def welcome(self):
        if not self.welcome_message_sent:
            self.welcome_message_sent = True
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("Начать тест",color=VkKeyboardColor.POSITIVE)
            keyboard.add_button("Мем", color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()
            keyboard.add_button("Статистика", color=VkKeyboardColor.PRIMARY)
            keyboard.add_button("Загрузить мем", color=VkKeyboardColor.SECONDARY)
            return Answer("Привет вездекодерам!", keyboard=keyboard)
        else:
            return Answer("Привет еще раз!")


    def help(self):
        return Answer("Список доступных команд:\n\n"
                      "начать тест\n"
                      "показать мем\n"
                      "статистика\n"
                      "загрузить мем\n"
                      "вернуться в начало | начало")


    def test(self, text):
        self.next_task = "test"

        if self.current_quesion == 0:
            return Answer("1")


    def show_meme(self, text):
        #self.next_task = "show_meme"
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button("Заебись", color=VkKeyboardColor.POSITIVE)
        keyboard.add_button("Хуево", color=VkKeyboardColor.NEGATIVE)
        return Answer("https://youtu.be/oDwPqhfwx64", keyboard=keyboard)


    def show_stat(self, text):
        #self.next_task = "show_stat"
        return Answer("Функция пока не доступна")


    def upload_meme(self, text):
        #self.next_task = "upload_meme"
        return Answer("Функция пока не доступна")
