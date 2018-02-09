from analytics import db_conn, config, app
from analytics.models import Chargebacks
from sqlalchemy import desc, create_engine, func, select, engine
from sqlalchemy.sql import text
from sshtunnel import SSHTunnelForwarder
import MySQLdb as db

class ChargebacksReplicator:

    def replicate_sd_chargebacks(self):
        app.logger.info('Starting replication on SD')
        account_name = config['sd_account_name']
        last_id = select([func.max(Chargebacks.c.original_id)]).where(Chargebacks.c.account == account_name).execute().first()
        last_id = last_id[0] if last_id[0] else 0

        connection_string = config['sd_connection_string'] + '?charset=utf8'
        source_engine = create_engine(connection_string)
        source_conn = source_engine.connect()
        sql = text('''SELECT maxpay_chargeback_new.*, maxpay_charge_new.merchant_user_id FROM maxpay_chargeback_new
            JOIN maxpay_charge_new ON maxpay_chargeback_new.base_reference = maxpay_charge_new.reference
            WHERE maxpay_chargeback_new.id > :last_id
            ORDER BY maxpay_chargeback_new.id ASC
            LIMIT :count''')
        result = source_conn.execute(sql, last_id=int(last_id), count=100).fetchall()

        chargebacks = []
        for chargeback in result:
            sql = text('''SELECT temp_users.webid as webid, webid.country AS country FROM temp_users
                JOIN webid ON webid.web_id = temp_users.webid
                WHERE temp_users.cust_id = :customer_id''')
            user_info = source_conn.execute(sql, customer_id=chargeback['merchant_user_id']).first()

            if not user_info:
                sql = text('''SELECT users.webid AS webid, webid.country AS country FROM users
                    JOIN webid ON webid.web_id = users.webid
                    WHERE users.customer_id = :customer_id''')
                user_info = source_conn.execute(sql, customer_id=chargeback['merchant_user_id']).first()

            if not user_info:
                user_info = dict(webid=None, country=None)

            chargeback_temp = dict(chargeback)
            chargeback_temp['webid'] = user_info['webid']
            chargeback_temp['webid_country'] = user_info['country']
            chargebacks.append(chargeback_temp)

        source_conn.close()

        values = []
        for chargeback in chargebacks:
            app.logger.info('Inserting chargeback id = %i, account = %s' % (chargeback ['id'], account_name))
            values.append(dict(account=account_name, merchant_user_id=chargeback['merchant_user_id'], webid=chargeback['webid'],
                country=chargeback['webid_country'], original_id=chargeback['id'], status=chargeback['status'], type=chargeback['type'],
                mode=chargeback['mode'], amount=chargeback['amount'], bank_time=chargeback['bank_time'],
                currency=chargeback['currency'], bank_id=chargeback['bank_id'], bank_authcode=chargeback['bank_authcode'],
                bank_update_time=chargeback['bank_update_time'],reference=chargeback['reference'], base_reference=chargeback['base_reference'],
                transaction_unique_id=chargeback['transaction_unique_id'], created_at=chargeback['date_created'], custom_mid_name=chargeback['custom_mid_name'],
                response=chargeback['charge_response'], time=chargeback['time']))

        if values:
            db_conn.execute(Chargebacks.insert(), values)

        app.logger.info('Finished replication on SD')

    def replicate_bb_chargebacks(self):
        app.logger.info('Starting replication on BB')
        account_name = config['bb_account_name']
        last_id = select([func.max(Chargebacks.c.original_id)]).where(Chargebacks.c.account == account_name).execute().first()
        last_id = last_id[0] if last_id[0] else 0

        connection_string = config['bb_connection_string'] + '?charset=utf8'
        source_engine = create_engine(connection_string)
        source_conn = source_engine.connect()
        sql = text('''SELECT maxpay_chargeback_new.*, maxpay_charge_new.merchant_user_id FROM maxpay_chargeback_new
            JOIN maxpay_charge_new ON maxpay_chargeback_new.base_reference = maxpay_charge_new.reference
            WHERE maxpay_chargeback_new.id > :last_id
            ORDER BY maxpay_chargeback_new.id ASC
            LIMIT :count''')
        result = source_conn.execute(sql, last_id=int(last_id), count=100).fetchall()

        chargebacks = []
        for chargeback in result:
            sql = text('''SELECT temp_users.webid as webid, webid.country AS country FROM temp_users
                JOIN webid ON webid.web_id = temp_users.webid
                WHERE temp_users.cust_id = :customer_id''')
            user_info = source_conn.execute(sql, customer_id=chargeback['merchant_user_id']).first()

            if not user_info:
                sql = text('''SELECT users.webid AS webid, webid.country AS country FROM users
                    JOIN webid ON webid.web_id = users.webid
                    WHERE users.customer_id = :customer_id''')
                user_info = source_conn.execute(sql, customer_id=chargeback['merchant_user_id']).first()

            if not user_info:
                user_info = dict(webid=None, country=None)

            chargeback_temp = dict(chargeback)
            chargeback_temp['webid'] = user_info['webid']
            chargeback_temp['webid_country'] = user_info['country']
            chargebacks.append(chargeback_temp)

        source_conn.close()

        values = []
        for chargeback in chargebacks:
            app.logger.info('Inserting chargeback id = %i, account = %s' % (chargeback ['id'], account_name))
            values.append(dict(account=account_name, merchant_user_id=chargeback['merchant_user_id'], webid=chargeback['webid'],
                country=chargeback['webid_country'], original_id=chargeback['id'], status=chargeback['status'], type=chargeback['type'],
                mode=chargeback['mode'], amount=chargeback['amount'], bank_time=chargeback['bank_time'],
                currency=chargeback['currency'], bank_id=chargeback['bank_id'], bank_authcode=chargeback['bank_authcode'],
                bank_update_time=chargeback['bank_update_time'],reference=chargeback['reference'], base_reference=chargeback['base_reference'],
                transaction_unique_id=chargeback['transaction_unique_id'], created_at=chargeback['date_created'], custom_mid_name=chargeback['custom_mid_name'],
                response=chargeback['charge_response'], time=chargeback['time']))

        if values:
            db_conn.execute(Chargebacks.insert(), values)

        app.logger.info('Finished replication on BB')

    def replicate_pb_chargebacks(self):
        app.logger.info('Starting replication on PB')
        account_name = config['pb_account_name']
        last_id = select([func.max(Chargebacks.c.original_id)]).where(Chargebacks.c.account == account_name).execute().first()
        last_id = last_id[0] if last_id[0] else 0

        chargebacks = []
        with SSHTunnelForwarder(
            (config['pb_ssh_host'], int(config['pb_ssh_port'])),
            ssh_username=config['pb_ssh_username'],
            ssh_password=config['pb_ssh_password'],
            remote_bind_address=('127.0.0.1', 3306),
            local_bind_address = ('127.0.0.1', 3307),
            ) as server:

            connection_string = config['pb_connection_string'] + '?charset=utf8'
            source_engine = create_engine(connection_string)
            source_conn = source_engine.connect()

            sql = text('''SELECT maxpay_chargeback_new.*, maxpay_charge_new.merchant_user_id FROM maxpay_chargeback_new
                JOIN maxpay_charge_new ON maxpay_chargeback_new.base_reference = maxpay_charge_new.reference
                WHERE maxpay_chargeback_new.id > :last_id
                ORDER BY maxpay_chargeback_new.id ASC
                LIMIT :count''')
            result = source_conn.execute(sql, last_id=int(last_id), count=100).fetchall()

            for chargeback in result:
                sql = text('''SELECT temp_users.webid as webid, webid.country AS country FROM temp_users
                    JOIN webid ON webid.web_id = temp_users.webid
                    WHERE temp_users.cust_id = :customer_id''')
                user_info = source_conn.execute(sql, customer_id=chargeback['merchant_user_id']).first()

                if not user_info:
                    sql = text('''SELECT users.webid AS webid, webid.country AS country FROM users
                        JOIN webid ON webid.web_id = users.webid
                        WHERE users.customer_id = :customer_id''')
                    user_info = source_conn.execute(sql, customer_id=chargeback['merchant_user_id']).first()

                if not user_info:
                    user_info = dict(webid=None, country=None)

                chargeback_temp = dict(chargeback)
                chargeback_temp['webid'] = user_info['webid']
                chargeback_temp['webid_country'] = user_info['country']
                chargebacks.append(chargeback_temp)

            source_conn.close()

        values = []
        for chargeback in chargebacks:
            app.logger.info('Inserting chargeback id = %i, account = %s' % (chargeback ['id'], account_name))
            values.append(dict(account=account_name, merchant_user_id=chargeback['merchant_user_id'], webid=chargeback['webid'],
                country=chargeback['webid_country'], original_id=chargeback['id'], status=chargeback['status'], type=chargeback['type'],
                mode=chargeback['mode'], amount=chargeback['amount'], bank_time=chargeback['bank_time'],
                currency=chargeback['currency'], bank_id=chargeback['bank_id'], bank_authcode=chargeback['bank_authcode'],
                bank_update_time=chargeback['bank_update_time'],reference=chargeback['reference'], base_reference=chargeback['base_reference'],
                transaction_unique_id=chargeback['transaction_unique_id'], created_at=chargeback['date_created'], custom_mid_name=chargeback['custom_mid_name'],
                response=chargeback['charge_response'], time=chargeback['time']))

        if values:
            db_conn.execute(Chargebacks.insert(), values)

        app.logger.info('Finished replication on PB')
