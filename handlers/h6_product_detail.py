from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile
from pyexpat.errors import messages

from bot_utils.message_utils import text_for_caption
from database.utils import db_get_product_by_id, db_get_user_cart, db_update_to_cart
from keyboards.inline_kb import cart_quantity_controller
from keyboards.reply_kb import back_arrow_button, phone_button

router = Router()


@router.callback_query(F.data.contains('product_'))
async def show_detail_product_info(callback: CallbackQuery, bot: Bot):
    """Показ детальной информации о продукте"""

    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    product_id = int(callback.data.split('_')[-1])
    product = db_get_product_by_id(product_id)
    user_cart = db_get_user_cart(chat_id)
    product_image = FSInputFile(path=product.image)

    print(product_image)

    if user_cart:
        db_update_to_cart(price=product.price, cart_id=user_cart.id)

        caption = text_for_caption(product.product_name, product.description, product.price)
        product_image = FSInputFile(path=product.image)

        await bot.send_message(
            chat_id=chat_id,
            text='Вы можете выбрать количество товара и добавить его в корзину',
            reply_markup=back_arrow_button()
        )

        await bot.send_photo(
            chat_id=chat_id,
            photo=product_image,
            caption=caption,
            parse_mode='HTML',
            reply_markup=cart_quantity_controller()
        )
