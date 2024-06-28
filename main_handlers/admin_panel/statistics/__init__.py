__all__ = ['statistics_router']

from aiogram import Router, F

from states.main_bot import Statistics

from .menu import statistics_menu
from .statistics_users import statistics_users, get_username, download_users
from .admin_statistics_shops import statistics_shops, get_username_shops, admin_statistics_shops, download_statistics
from .all_statistics_time_line import all_get_period, all_statistics_time_line
from .statistics_time_line import get_period, get_name_shop, statistics_time_line

statistics_router = Router()

statistics_router.callback_query.register(statistics_menu, F.data == "admin_statistics")

statistics_router.callback_query.register(statistics_users, F.data == "admin_statistics_users")
statistics_router.message.register(get_username, F.text, Statistics.users)
statistics_router.callback_query.register(download_users, F.data == "download_users")

statistics_router.callback_query.register(statistics_shops, lambda x: x.data.startswith("allAdminStatistics_"))
statistics_router.message.register(get_username_shops, F.text, Statistics.shops)
statistics_router.callback_query.register(admin_statistics_shops, lambda x: x.data.startswith("adminStatistics_"))
statistics_router.callback_query.register(download_statistics, lambda x: x.data.startswith("download_statistics_"))

statistics_router.callback_query.register(all_statistics_time_line, F.data == "admin_all_statistics_time_line")
statistics_router.message.register(all_get_period, F.text, Statistics.allPeriod)

statistics_router.callback_query.register(get_name_shop, F.data == "admin_statistics_time_line")
statistics_router.message.register(statistics_time_line, F.text, Statistics.shop_period)
statistics_router.message.register(get_period, F.text, Statistics.period)
