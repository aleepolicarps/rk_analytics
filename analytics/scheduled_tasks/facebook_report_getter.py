from analytics import app, config, db_conn
from analytics.models import FacebookAdReports
from facebookads.api import FacebookAdsApi
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adaccountuser import AdAccountUser
from facebookads.adobjects.campaign import Campaign
from facebookads.adobjects.adset import AdSet
from facebookads.adobjects.ad import Ad
from datetime import datetime, timedelta
import pytz


import json
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)


class FacebookReportGetter:

    def __init__(self):
        FacebookAdsApi.init(config['facebook_app_id'], config['facebook_app_secret'], config['facebook_access_token'])

    def get_budgetbear_report(self):
        ad_account = AdAccount(config['facebook_bb_ad_account_id'])
        mnl_now = datetime.now(pytz.timezone('Asia/Hong_Kong'))
        for campaign in ad_account.get_campaigns():
            insights = campaign.get_insights(params={
                'level': 'ad',
                'date_preset': 'yesterday',
                'breakdowns': ['hourly_stats_aggregated_by_advertiser_time_zone']
            }, fields=[
                'impressions', 'inline_link_clicks', 'inline_link_click_ctr', 'relevance_score', 'spend',
                'campaign_name', 'adset_name', 'ad_name', 'actions', 'date_start', 'date_stop',
                'clicks', 'cpc', 'cpm', 'ctr',
            ])

            for insight in insights:
                hour_range = insight['hourly_stats_aggregated_by_advertiser_time_zone']

                time_from = hour_range.split(' - ')[0]
                time_to = hour_range.split(' - ')[1]

                mnl_time_from = insight.get('date_start') + ' ' + time_from
                mnl_time_to = insight.get('date_stop') + ' ' + time_to

                mnl_time_from = datetime.strptime(mnl_time_from, '%Y-%m-%d %H:%M:%S')
                mnl_time_to = datetime.strptime(mnl_time_to, '%Y-%m-%d %H:%M:%S')

                denmark_time_from = pytz.timezone('Asia/Hong_Kong').localize(mnl_time_from).astimezone(pytz.timezone('Europe/Copenhagen'))
                denmark_time_to = pytz.timezone('Asia/Hong_Kong').localize(mnl_time_to).astimezone(pytz.timezone('Europe/Copenhagen'))

                offsite_conversion = 0
                complete_registrations = 0
                relevance_score = insight.get('relevance_score').get('score') if insight.get('relevance_score') else 0
                actions = insight.get('actions') if insight.get('actions') else []
                for action in actions:
                    if action['action_type'] == 'offsite_conversion':
                        offsite_conversion = action['value']
                    elif action['action_type'] == 'offsite_conversion.fb_pixel_complete_registration':
                        complete_registrations = action['value']

                db_conn.execute(FacebookAdReports.insert(), account='budgetbear.net', campaign_name=insight.get('campaign_name'),
                                ad_set_name=insight.get('adset_name'), ad_name=insight.get('ad_name'), account_currency='USD',
                                clicks=insight.get('clicks'), cpc=insight.get('cpc'), cpm=insight.get('cpm'), ctr=insight.get('ctr'),
                                impressions=insight.get('impressions'), inline_link_clicks=insight.get('inline_link_clicks'),
                                inline_link_click_ctr=insight.get('inline_link_click_ctr'), spend=insight.get('spend'), relevance_score=relevance_score,
                                offsite_conversion=offsite_conversion, complete_registrations=complete_registrations, since=denmark_time_from, until=denmark_time_to)
