import datetime

from database.commands import Database
from config.config import schedular, TZ
from utils.schedular import send_mail


async def recover_mails():
    mails = await Database.Mail.get_waiting_mails()
    for mail in mails:
        if mail.wait_date.timestamp() >= datetime.datetime.now(TZ).timestamp():
            schedular.add_job(func=send_mail, trigger="date", id=f"mail_{mail.id}", args=(mail.id,),
                              next_run_time=mail.wait_date)
        else:
            await Database.Mail.update_status(mail.id, "cancel")
