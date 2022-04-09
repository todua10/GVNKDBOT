import vk_api, words, cfg
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
from vk_api.utils import get_random_id
import _pickle as pickle

class Question:
    def __init__(self):
        self

def question_keyboard(question):
    keyboard = VkKeyboard(one_time=True)
    for answer in question:
        keyboard.add_button(answer, color=VkKeyboardColor.SECONDARY)
