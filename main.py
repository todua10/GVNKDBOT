import vk_api, words, cfg
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
from  vk_api.utils import get_random_id

vk_session = vk_api.VkApi(token=cfg.access_token)
vk_longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

keyboard = VkKeyboard(one_time=True)

keyboard.add_button('1', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('2', color=VkKeyboardColor.PRIMARY)


for event in vk_longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and event.from_user:
            if event.text.lower() in words.hello:
                vk.messages.send(user_id=event.user_id, message="Привет вездекодерам!",
                                 random_id=get_random_id(),
                                 keyboard=keyboard.get_keyboard())
