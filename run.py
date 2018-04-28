import service
import sales
import doctor
import patient
import tencent_ent_login
import tencent_service_login
import util
import logging
from threading import Thread
import time


def sync_add_doctor_tag():
    while True:
        try:
            conn = service.db_pool.connection()
            cursor = conn.cursor()
            cursor.execute(
                'select doctor_id,open_id from doctor where is_add_tag is null and open_id is not null')
            rows = cursor.fetchall()
            for row in rows:
                if tencent_service_login.set_user_tag(row[1], 'doctor'):
                    cursor.execute('update doctor set is_add_tag = 1 where doctor_id=%(doctor_id)s', {
                        'doctor_id': row[0]})
            cursor.close()
            conn.close()
        finally:
            print('continue')
            time.sleep(3)


#sync_task = Thread(target=sync_add_doctor_tag)
# sync_task.start()
#logging.basicConfig(filename='service.log', level=logging.DEBUG)
service.web_app.run(debug=False)
