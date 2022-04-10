import vk_api, cfg

from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
from  vk_api.utils import get_random_id
from bot import Bot
from bot import Answer

# Авторизация
vk_session = vk_api.VkApi(token=cfg.access_token2)
vk_longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
upload = VkUpload(vk_session)


# Универсальный метод
def send_message(id, text, answers=None, one_time=True, inline=False, keyboard=None, attachments = None):
    if not answers and not keyboard and not attachments:
        send_text(id, text)
    elif answers and not keyboard and not attachments:
        send_easy_keyboard(id, text, answers, one_time, inline)
    elif keyboard and not attachments:
        send_keyboard(id, text, keyboard)
    elif answers and attachments:
        keyboard = easy_keyboard(answers, one_time, inline)
        send_message(user_id=id, message=text, random_id=get_random_id(), keyboard=keyboard, attachments=attachments)
    elif keyboard and attachments:
        send_message(user_id=id, message=text, random_id=get_random_id(), keyboard=keyboard, attachments=attachments)
    elif attachments:
        send_attachments(id, text, attachments)

# Упрощенные, более безопасные методы
def send_text(id, text):
    vk.messages.send(user_id=id, message=text, random_id=get_random_id())

# Упрощенное создание сообщения с клавиатурой
def send_easy_keyboard(id, text, answers, one_time=True, inline=False):
    keyboard = easy_keyboard(answers, one_time, inline)
    if validate_keyboard(keyboard):
        vk.messages.send(user_id=id, message=text,
                         random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard())

# Отправление сообщения с клавиатурой
def send_keyboard(id, text, keyboard):
    if validate_keyboard(keyboard):
        vk.messages.send(user_id=id, message=text,
                         random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard())


def send_attachments(id, text, attachments):
    vk.messages.send(user_id=id, message=text, random_id=get_random_id(), attachment=','.join(attachments))



# Проверка соответсвия клавиатуры ограничениям
def validate_keyboard(keyboard):
    if not keyboard:
        return False
    # Для не inline клавиатур макс 5 кнопок в ряду, макс 10 рядов, макс всего 40 кнопок
    # Для inline клавиатур макс 5 кнопок в ряду, макс 6 рядов, макс всего 10 кнопок
    if len(keyboard.lines)>10 and not keyboard.inline or len(keyboard.lines)>6 and keyboard.inline:
        return False
    if keyboard.inline and keyboard.one_time: # inline клавиатура не может быть one_time
        return False
    if type(keyboard) is vk_api.keyboard.VkKeyboard:
        return True


# При передаче массива элементов, возвращает клавиатуру с распределёнными кнопками
def easy_keyboard(answers=None, one_time=True, inline=False):
    one_time = one_time if not inline else False  # inline клавиатура не может быть one_time
    keyboard = VkKeyboard(one_time=one_time, inline=inline)

    if len(answers)>40 and not keyboard.inline or len(answers)>10 and keyboard.inline:
        return

    d = 5
    for i in [5, 4, 3, 2]:  # Код для красивого расположения кнопок в рядах
        if len(answers) % i == 0:  # Допускается макс 5 кнопок в одном ряду
            d = i
            break

    for i in range(len(answers)):
        keyboard.add_button(answers[i], color=VkKeyboardColor.SECONDARY)
        if (i + 1) % d == 0 and i != len(answers) - 1:  # Проверка на необходимость добавления нового ряда кнопок
            keyboard.add_line()
    return keyboard


# Словарь работяг, созданных под каждого пользователя
bots = {}

# Работяги идут на работу
for event in vk_longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.from_user:
        if event.user_id not in bots: # Если пользователь обращается впервые, создает новый экземпляр работяги (ключ - id пользователя)
            bots[event.user_id] = Bot(event.user_id)

        bot_ans = bots[event.user_id].update(event.text)
        send_message(event.user_id, bot_ans.text, bot_ans.answers, bot_ans.one_time, bot_ans.inline, bot_ans.keyboard, bot_ans.attachments)