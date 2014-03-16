import httplib2
import smtplib
import urllib


class Notifier(object):
    def __init__(self, series, season, episode):
        self.series = series
        self.season = str(season)
        self.episode = str(episode)


class EmailNotifier(Notifier):
    def __init__(self, series, season, episode, params):

        super(EmailNotifier, self).__init__(series, season, episode)

        # TODO Validate parameters are provided
        self.mail_server = params['mail_server']
        self.mail_port = params['mail_port']
        self.mail_account = params['mail_account']
        self.mail_password = params['mail_password']
        self.mail_to = params['mail_to']
        self.mail_from = params['mail_from']

    def notify(self):
        subject = 'New episode of ' + self.series
        body = 'A new episode of ' + self.series + ' is available (Season ' + self.season + ', episode ' + self.episode + ')'

        headers = ['From: ' + self.mail_from,
                   'Subject: ' + subject,
                   'To: ' + self.mail_to,
                   'MIME-Version: 1.0',
                   'Content-Type: text/html']
        headers = '\r\n'.join(headers)

        session = smtplib.SMTP(self.mail_server, self.mail_port)
        session.ehlo()
        session.starttls()
        session.login(self.mail_account, self.mail_password)
        session.sendmail(self.mail_from, self.mail_to, headers + '\r\n\r\n' + body)
        session.quit()


class TodoNotifier(Notifier):

    todo_api_url = 'https://todoist.com/API'

    def __init__(self, series, season, episode, params):
        super(TodoNotifier, self).__init__(series, season, episode)

        # TODO Validate parameter is provided
        self.todo_api_key = params['todo_api_key']

    def notify(self):
        content = 'Watch ' + self.series + ', episode ' + self.episode + ' from season ' + self.season

        url = self.todo_api_url + '/addItem?token=' + self.todo_api_key + '&content=' + urllib.quote_plus(content)

        h = httplib2.Http()
        h.request(url, 'GET')