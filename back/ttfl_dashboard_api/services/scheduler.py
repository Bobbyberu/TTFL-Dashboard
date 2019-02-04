from apscheduler.schedulers.background import BackgroundScheduler
from db_controller import insert_all_boxscores, insert_all_teams, insert_all_players
from datetime import datetime
from services.logger import getLogger

logger = getLogger(__name__)


def insert_live_boxscores():
    logger.info('Beginning live boxscores inserting...')
    utcnow = datetime.utcnow()
    insert_all_boxscores(utcnow.year, utcnow.month, utcnow.day)
    logger.info('Live boxscores inserted')


def init_scheduler():
    scheduler = BackgroundScheduler()
    # insert live boxscores every 5 minutes during night from 6pm from 7am
    scheduler.add_job(insert_live_boxscores, 'cron', year='*', month='*',
                      day='*', week='*', hour='18-23', minute='*/1', second='0', id='live_boxscores_evening')
    scheduler.add_job(insert_live_boxscores, 'cron', year='*', month='*',
                      day='*', week='*', hour='0-6', minute='*/1', second='0', id='live_boxscores_morning')

    # update all teams every day at 8am
    scheduler.add_job(insert_all_teams, 'cron', year='*', month='*',
                      day='*', week='*', hour='8', minute='0', second='0', id='daily_teams_update')

    # update all players every day at 8:10am
    scheduler.add_job(insert_all_players, 'cron', year='*', month='*',
                      day='*', week='*', hour='8', minute='10', second='0', id='daily_players_update')

    scheduler.start()
