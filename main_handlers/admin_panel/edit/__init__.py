__all__ = ['router']

from aiogram import Router, F

from states.main_bot import EditCount, EditCategory, EditSubcategory, EditGood

from .edit_category import (edit_category, edit_name_category, get_edit_name_category, edit_description_category,
                            get_edit_description_category, edit_weight_category, get_edit_weight_category,
                            get_edit_photo_category, edit_photo_category, delete_photo_category)
from .edit_subcategory import (edit_subcategory, edit_name_subcategory, get_edit_name_subcategory,
                               edit_description_subcategory, get_edit_description_subcategory)
from .edit_good import (edit_good_count, get_edit_good_count, edit_good_price, get_edit_good_price,
                        edit_good_description, get_edit_good_description, edit_good_name, get_edit_good_name,
                        edit_good_product, get_edit_good_product, edit_good_weight, get_edit_good_weight)

router = Router()

router.callback_query.register(edit_category, lambda x: x.data.startswith("edit_category_"))
router.callback_query.register(edit_name_category, lambda x: x.data.startswith("edit_name_"))
router.message.register(get_edit_name_category, F.text, EditCategory.name)
router.callback_query.register(edit_weight_category, lambda x: x.data.startswith("edit_weight_"))
router.message.register(get_edit_weight_category, F.text, EditCategory.weight)
router.callback_query.register(edit_description_category, lambda x: x.data.startswith("edit_description_"))
router.message.register(get_edit_description_category, F.text, EditCategory.description)
router.callback_query.register(edit_photo_category, lambda x: x.data.startswith("edit_photo_"))
router.message.register(get_edit_photo_category, F.photo, EditCategory.photo)
router.callback_query.register(delete_photo_category, F.data == "delete_photo")

router.callback_query.register(edit_subcategory, lambda x: x.data.startswith("edit_subcategory_"))
router.callback_query.register(edit_name_subcategory, lambda x: x.data.startswith("edit_sub_name_"))
router.message.register(get_edit_name_subcategory, F.text, EditSubcategory.name)
router.callback_query.register(edit_description_subcategory,
                               lambda x: x.data.startswith("edit_sub_description_"))
router.message.register(get_edit_description_subcategory, F.text, EditSubcategory.description)

router.callback_query.register(edit_good_count, lambda x: x.data.startswith("edit_good_count_"))
router.message.register(get_edit_good_count, F.text, EditGood.count)
router.callback_query.register(edit_good_price, lambda x: x.data.startswith("edit_good_price_"))
router.message.register(get_edit_good_price, F.text, EditGood.price)
router.callback_query.register(edit_good_name, lambda x: x.data.startswith("edit_good_name_"))
router.message.register(get_edit_good_name, F.text, EditGood.name)
router.callback_query.register(edit_good_description, lambda x: x.data.startswith("edit_good_description_"))
router.message.register(get_edit_good_description, F.text, EditGood.description)
router.callback_query.register(edit_good_product, lambda x: x.data.startswith("edit_good_product_"))
router.message.register(get_edit_good_product, F.text, EditGood.product)
router.callback_query.register(edit_good_weight, lambda x: x.data.startswith("edit_good_weight_"))
router.message.register(get_edit_good_weight, F.text, EditGood.weight)
