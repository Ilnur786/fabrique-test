from sqlalchemy.orm import scoped_session
from datetime import datetime
from db_api import SessionLocal
from db_api import Distribution, Client, Message
from extension import dynamic_update
import requests as req
from envparse import env
import time


def main():
    env.read_envfile('config/.env.dev')
    TOKEN = env.str('JWT_TOKEN')
    db_session = scoped_session(SessionLocal)
    send_status_cases = ['SENT', 'NOT_SENT', 'FAIL']
    s = req.session()
    while True:
        distrs = db_session.query(Distribution).filter(Distribution.end_date >= datetime.now()).all()
        if distrs:
            for distr in distrs:
                clients = db_session.query(Client).filter_by(tag=distr.client_filter).all()
                for client in clients:
                    msg = db_session.query(Message).filter_by(distribution_id=distr.id, client_id=client.id).first()
                    if msg is None:
                        msg = Message(distribution_id=distr.id, client_id=client.id)
                        db_session.add(msg)
                        db_session.flush()
                    elif msg.send_status == 'SENT':
                        continue
                    payload = {
                        "id": msg.id,
                        "phone": client.mobile_number,
                        "text": distr.text
                    }
                    r = s.post(url=f'https://probe.fbrq.cloud/v1/send/{msg.id}', json=payload,
                               headers={"Content-Type": "application/json", "Authorization": TOKEN})
                    if r.status_code == 200:
                        msg.send_status = "SENT"
                        msg.send_date = datetime.now()
                    else:
                        msg.send_status = "FAIL"
                    db_session.commit()
        time.sleep(30)


if __name__ == '__main__':
    main()
