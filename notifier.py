# -*- coding: utf-8-*-
import Queue
import atexit
from modules import Gmail
from modules import Liveticker
from apscheduler.schedulers.background import BackgroundScheduler
import logging


class Notifier(object):

    class NotificationClient(object):

        def __init__(self, gather, timestamp):
            self.gather = gather
            self.timestamp = timestamp

        def run(self):
            self.timestamp = self.gather(self.timestamp)

    def __init__(self, profile):
        self._logger = logging.getLogger(__name__)
        self.q = Queue.Queue()
        self.profile = profile
        self.notifiers = []

        if 'gmail_address' in profile and 'gmail_password' in profile:
            self.notifiers.append(self.NotificationClient(
                self.handleEmailNotifications, None))
        else:
            self._logger.warning('gmail_address or gmail_password not set ' +
                                 'in profile, Gmail notifier will not be used')

        if 'Liveticker' in profile and 'Team' in profile['Liveticker'] and 'Liga' in profile['Liveticker']:
            self.notifiers.append(self.NotificationClient(
                self.handleLivetickerNotifications, 0))
        else:
            self._logger.warning('Liveticker information not set, Liveticker notifier will not be used')

        sched = BackgroundScheduler(timezone="UTC", daemon=True)
        sched.start()
        sched.add_job(self.gather, 'interval', seconds=30)
        atexit.register(lambda: sched.shutdown(wait=False))

    def gather(self):
        [client.run() for client in self.notifiers]

    def handleEmailNotifications(self, lastDate):
        """Places new Gmail notifications in the Notifier's queue."""
        emails = Gmail.fetchUnreadEmails(self.profile, since=lastDate)
        if emails:
            lastDate = Gmail.getMostRecentDate(emails)

        def styleEmail(e):
            return "New email from %s." % Gmail.getSender(e)

        for e in emails:
            self.q.put(styleEmail(e))

        return lastDate
        
    def handleLivetickerNotifications(self, latest):
        """ Gets the new goal from the game and places it in the Notifier's queue.
            latest ist die letzte GoalID von OpenLigaDB, standardmäßig: 0
        """
        team = self.profile["Liveticker"]["Team"]
        liga = self.profile["Liveticker"]["Liga"]
        lt = Liveticker(team, liga)
        ergebnis = lt.getErgebnis()
        
        if ergebnis:
            letztesTor = lt.getLetztesTor(ergebnis)
            
            if letztesTor["GoalID"] > latest:
                self.q.put(Liveticker.formatiereTor(letztesTor))
                latest = letztesTor["GoalID"]
        
        return latest
        
    def getNotification(self):
        """Returns a notification. Note that this function is consuming."""
        try:
            notif = self.q.get(block=False)
            return notif
        except Queue.Empty:
            return None

    def getAllNotifications(self):
        """
            Return a list of notifications in chronological order.
            Note that this function is consuming, so consecutive calls
            will yield different results.
        """
        notifs = []

        notif = self.getNotification()
        while notif:
            notifs.append(notif)
            notif = self.getNotification()

        return notifs