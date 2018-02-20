from analytics import db_conn, config, app
from analytics.models import LogData
from sqlalchemy import desc, create_engine, func, select, engine
from sqlalchemy.sql import text
from sshtunnel import SSHTunnelForwarder
import MySQLdb as db


class LogDataReplicator:

    def replicate_sd_log_data(self):
        app.logger.info('Starting replication on SD log_data')
        account_name = config['sd_account_name']
        last_id = select([func.max(LogData.c.original_id)]).where(LogData.c.account == account_name).execute().first()
        last_id = last_id[0] if last_id[0] else 0

        connection_string = config['sd_connection_string'] + '?charset=utf8'
        source_engine = create_engine(connection_string)
        source_conn = source_engine.connect()
        sql = text('''SELECT * FROM log_data
            WHERE log_data.id > :last_id
                AND log_data.created_date > '2017-12-31 23:59:59'
            ORDER BY log_data.id ASC
            LIMIT :count''')
        result = source_conn.execute(sql, last_id=int(last_id), count=400).fetchall()

        log_data = []
        for datum in result:
            sql = text('''SELECT country FROM webid WHERE web_id = :webid''')
            webid_info = source_conn.execute(sql, webid=datum['webid']).first()

            if not webid_info:
                webid_info = dict(country=None)

            log_data_temp = dict(datum)
            log_data_temp['country'] = webid_info['country']
            log_data.append(log_data_temp)

        source_conn.close()

        values = []
        for datum in log_data:
            app.logger.info('Inserting log_data id = %i, account = %s' % (datum['id'], account_name))
            values.append(dict(account=account_name, step=datum['step'], customer_id=datum['cust_id'], email=datum['email'],
                               fname=datum['fname'], lname=datum['lname'], webid=datum['webid'], country=datum['country'], pubid=datum['pubid'],
                               subid=datum['subid'], utm_medium=datum['utm_medium'], utm_term=datum['utm_term'], utm_content=datum['utm_content'],
                               utm_campaign=datum['utm_campaign'], referrer_url=datum['referrer_url'], ip_address=datum['ip_addr'],
                               click_id=datum['click_id'], user_agent=datum['user_agent'], original_id=datum['id'], created_at=datum['created_date']))

        if values:
            db_conn.execute(LogData.insert(), values)

        app.logger.info('Finished replication on SD log_data')

    def replicate_bb_log_data(self):
        app.logger.info('Starting replication on BB log_data')
        account_name = config['bb_account_name']
        last_id = select([func.max(LogData.c.original_id)]).where(LogData.c.account == account_name).execute().first()
        last_id = last_id[0] if last_id[0] else 0

        connection_string = config['bb_connection_string'] + '?charset=utf8'
        source_engine = create_engine(connection_string)
        source_conn = source_engine.connect()
        sql = text('''SELECT * FROM log_data
            WHERE log_data.id > :last_id
                AND log_data.created_date > '2017-12-31 23:59:59'
            ORDER BY log_data.id ASC
            LIMIT :count''')
        result = source_conn.execute(sql, last_id=int(last_id), count=400).fetchall()

        log_data = []
        for datum in result:
            sql = text('''SELECT country FROM webid WHERE web_id = :webid''')
            webid_info = source_conn.execute(sql, webid=datum['webid']).first()

            if not webid_info:
                webid_info = dict(country=None)

            log_data_temp = dict(datum)
            log_data_temp['country'] = webid_info['country']
            log_data.append(log_data_temp)

        source_conn.close()

        values = []
        for datum in log_data:
            app.logger.info('Inserting log_data id = %i, account = %s' % (datum['id'], account_name))
            values.append(dict(account=account_name, step=datum['step'], customer_id=datum['cust_id'], email=datum['email'],
                               fname=datum['fname'], lname=datum['lname'], webid=datum['webid'], country=datum['country'], pubid=datum['pubid'],
                               subid=datum['subid'], utm_medium=datum['utm_medium'], utm_term=datum['utm_term'], utm_content=datum['utm_content'],
                               utm_campaign=datum['utm_campaign'], referrer_url=datum['referrer_url'], ip_address=datum['ip_addr'],
                               click_id=datum['click_id'], user_agent=datum['user_agent'], original_id=datum['id'], created_at=datum['created_date']))

        if values:
            db_conn.execute(LogData.insert(), values)

        app.logger.info('Finished replication on BB log_data')

    def replicate_pb_log_data(self):
        app.logger.info('Starting replication on PB log_data')
        account_name = config['pb_account_name']
        last_id = select([func.max(LogData.c.original_id)]).where(LogData.c.account == account_name).execute().first()
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
            sql = text('''SELECT * FROM log_data
                WHERE log_data.id > :last_id
                    AND log_data.created_date > '2017-12-31 23:59:59'
                ORDER BY log_data.id ASC
                LIMIT :count''')
            result = source_conn.execute(sql, last_id=int(last_id), count=400).fetchall()

            log_data = []
            for datum in result:
                sql = text('''SELECT country FROM webid WHERE web_id = :webid''')
                webid_info = source_conn.execute(sql, webid=datum['webid']).first()

                if not webid_info:
                    webid_info = dict(country=None)

                log_data_temp = dict(datum)
                log_data_temp['country'] = webid_info['country']
                log_data.append(log_data_temp)

            source_conn.close()

        values = []
        for datum in log_data:
            app.logger.info('Inserting log_data id = %i, account = %s' % (datum['id'], account_name))
            values.append(dict(account=account_name, step=datum['step'], customer_id=datum['cust_id'], email=datum['email'],
                               fname=datum['fname'], lname=datum['lname'], webid=datum['webid'], country=datum['country'], pubid=datum['pubid'],
                               subid=datum['subid'], utm_medium=datum['utm_medium'], utm_term=datum['utm_term'], utm_content=datum['utm_content'],
                               utm_campaign=datum['utm_campaign'], referrer_url=datum['referrer_url'], ip_address=datum['ip_addr'],
                               click_id=datum['click_id'], user_agent=datum['user_agent'], original_id=datum['id'], created_at=datum['created_date']))

        if values:
            db_conn.execute(LogData.insert(), values)

        app.logger.info('Finished replication on PB log_data')
