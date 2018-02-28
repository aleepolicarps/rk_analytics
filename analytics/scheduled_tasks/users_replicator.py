from analytics import db_conn, config, app
from analytics.models import Users
from sqlalchemy import desc, create_engine, func, select, engine
from sqlalchemy.sql import text
from sshtunnel import SSHTunnelForwarder
from datetime import timedelta
import MySQLdb as db


class UsersReplicator:

    def replicate_sd_users(self):
        app.logger.info('Starting replication on SD users')
        account_name = config['sd_account_name']
        last_id = select([func.max(Users.c.original_id)]).where(Users.c.account == account_name).execute().first()
        last_id = last_id[0] if last_id[0] else 0

        connection_string = config['sd_connection_string'] + '?charset=utf8'
        source_engine = create_engine(connection_string)
        source_conn = source_engine.connect()
        sql = text('''SELECT * FROM users
            WHERE users.id > :last_id
            ORDER BY users.id ASC
            LIMIT :count''')
        result = source_conn.execute(sql, last_id=int(last_id), count=100).fetchall()

        users = []
        for user in result:
            sql = text('''SELECT country FROM webid WHERE web_id = :webid''')
            webid_info = source_conn.execute(sql, webid=user['webid']).first()

            if not webid_info:
                webid_info = dict(country=None)

            user_temp = dict(user)
            user_temp['country'] = webid_info['country'].title() if webid_info else None
            users.append(user_temp)

        source_conn.close()

        values = []
        for user in users:
            app.logger.info('Inserting users id = %i, account = %s' % (user['id'], account_name))
            created_at = user['created_date'] - timedelta(hours=1)
            values.append(dict(account=account_name, customer_id=user['customer_id'], email=user['email'],
                               fname=user['fname'], lname=user['lname'], webid=user['lname'], country=user['country'],
                               pubid=user['pubid'], subid=user['subid'], utm_medium=user['utm_medium'], utm_term=user['utm_term'],
                               utm_content=user['utm_content'], utm_campaign=user['utm_campaign'], referrer_url=user['referrer_url'],
                               ip_address=user['ip_addr'], click_id=user['click_id'], user_agent=user['user_agent'], original_id=user['id'],
                               created_at=created_at))
        if values:
            db_conn.execute(Users.insert(), values)

        app.logger.info('Finished replication on SD users')

    def replicate_bb_users(self):
        app.logger.info('Starting replication on BB users')
        account_name = config['bb_account_name']
        last_id = select([func.max(Users.c.original_id)]).where(Users.c.account == account_name).execute().first()
        last_id = last_id[0] if last_id[0] else 0

        connection_string = config['bb_connection_string'] + '?charset=utf8'
        source_engine = create_engine(connection_string)
        source_conn = source_engine.connect()
        sql = text('''SELECT * FROM users
            WHERE users.id > :last_id
            ORDER BY users.id ASC
            LIMIT :count''')
        result = source_conn.execute(sql, last_id=int(last_id), count=100).fetchall()

        users = []
        for user in result:
            sql = text('''SELECT country FROM webid WHERE web_id = :webid''')
            webid_info = source_conn.execute(sql, webid=user['webid']).first()

            if not webid_info:
                webid_info = dict(country=None)

            user_temp = dict(user)
            user_temp['country'] = webid_info['country'].title() if webid_info else None
            users.append(user_temp)

        source_conn.close()

        values = []
        for user in users:
            app.logger.info('Inserting users id = %i, account = %s' % (user['id'], account_name))
            created_at = user['created_date'] - timedelta(hours=1)
            values.append(dict(account=account_name, customer_id=user['customer_id'], email=user['email'],
                               fname=user['fname'], lname=user['lname'], webid=user['lname'], country=user['country'],
                               pubid=user['pubid'], subid=user['subid'], utm_medium=user['utm_medium'], utm_term=user['utm_term'],
                               utm_content=user['utm_content'], utm_campaign=user['utm_campaign'], referrer_url=user['referrer_url'],
                               ip_address=user['ip_addr'], click_id=user['click_id'], user_agent=user['user_agent'], original_id=user['id'],
                               created_at=created_at))
        if values:
            db_conn.execute(Users.insert(), values)

        app.logger.info('Finished replication on BB users')

    def replicate_pb_users(self):
        app.logger.info('Starting replication on PB users')
        account_name = config['pb_account_name']
        last_id = select([func.max(Users.c.original_id)]).where(Users.c.account == account_name).execute().first()
        last_id = last_id[0] if last_id[0] else 0

        log_data = []
        with SSHTunnelForwarder(
                (config['pb_ssh_host'], int(config['pb_ssh_port'])),
                ssh_username=config['pb_ssh_username'],
                ssh_password=config['pb_ssh_password'],
                remote_bind_address=('127.0.0.1', 3306),
                local_bind_address=('127.0.0.1', 3307)) as server:

            connection_string = config['pb_connection_string'] + '?charset=utf8'
            source_engine = create_engine(connection_string)
            source_conn = source_engine.connect()
            sql = text('''SELECT * FROM users
                WHERE users.id > :last_id
                ORDER BY users.id ASC
                LIMIT :count''')
            result = source_conn.execute(sql, last_id=int(last_id), count=100).fetchall()

            users = []
            for user in result:
                sql = text('''SELECT country FROM webid WHERE web_id = :webid''')
                webid_info = source_conn.execute(sql, webid=user['webid']).first()

                if not webid_info:
                    webid_info = dict(country=None)

                user_temp = dict(user)
                user_temp['country'] = webid_info['country'].title() if webid_info else None
                users.append(user_temp)

            source_conn.close()

        values = []
        for user in users:
            app.logger.info('Inserting users id = %i, account = %s' % (user['id'], account_name))
            created_at = user['created_date'] - timedelta(hours=1)
            values.append(dict(account=account_name, customer_id=user['customer_id'], email=user['email'],
                               fname=user['fname'], lname=user['lname'], webid=user['lname'], country=user['country'],
                               pubid=user['pubid'], subid=user['subid'], utm_medium=user['utm_medium'], utm_term=user['utm_term'],
                               utm_content=user['utm_content'], utm_campaign=user['utm_campaign'], referrer_url=user['referrer_url'],
                               ip_address=user['ip_addr'], click_id=user['click_id'], user_agent=user['user_agent'], original_id=user['id'],
                               created_at=created_at))
        if values:
            db_conn.execute(Users.insert(), values)

        app.logger.info('Finished replication on PB users')
