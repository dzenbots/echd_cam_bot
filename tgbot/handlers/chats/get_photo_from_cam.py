import os
import shutil
from io import BytesIO

import cv2
import requests
from PIL import Image
from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from requests.auth import HTTPDigestAuth

from tgbot import config
from tgbot.keyboards import GetBuildingCallBack, get_cameras_for_building_keyboard, GetBuildingCamerasCallback
from tgbot.states import GetPhotoState

photo_router = Router()


@photo_router.callback_query(GetPhotoState.get_building, GetBuildingCallBack.filter())
async def get_building_for_photo_from_cam(call: CallbackQuery,
                                          state: FSMContext,
                                          callback_data: GetBuildingCallBack,
                                          bot: Bot):
    building_address = callback_data.address
    building = [building for building in config.buildings if building.address == building_address][0]
    edited_message = await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=(await state.get_data()).get('edited_message'),
        text='Выберите камеру',
        reply_markup=None if building.cameras is [] else get_cameras_for_building_keyboard(building)
    )
    await state.set_state(GetPhotoState.get_camera)
    await state.set_data(
        {
            'edited_message': edited_message.message_id,
            'building_address': building.address,
        }
    )


@photo_router.callback_query(GetPhotoState.get_camera, GetBuildingCamerasCallback.filter())
async def get_camera_for_photo_from_cam(call: CallbackQuery,
                                        state: FSMContext,
                                        callback_data: GetBuildingCamerasCallback,
                                        bot: Bot):
    camera_name = callback_data.camera_name
    building_address = (await state.get_data()).get('building_address')
    building = [building for building in config.buildings if building.address == building_address][0]
    camera = [camera for camera in building.cameras if camera.name == camera_name][0]
    edited_message = await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=(await state.get_data()).get('edited_message'),
        text='Следующим сообщением Вы получите фото с камеры',
        reply_markup=None
    )
    camera_url = f'http://{camera.ip_address}/cgi-bin/snapshot.cgi?channel=1'
    auth = HTTPDigestAuth(username=camera.login, password=camera.password)
    response = requests.get(camera_url, auth=auth)
    print(response)
    if response.status_code == 200:
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        image.save("image.jpg")
    await bot.send_photo(
        chat_id=call.message.chat.id,
        photo=FSInputFile('image.jpg')
    )
    os.remove('image.jpg')
    await state.clear()
