import httplib2
import os
import re
import pickle

from apiclient import discovery
from apiclient import errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class Person():
    def __init__(self, raw=None):
        self.Name = None
        self.Address = None
        if raw is not None:
            self.__parse_raw(raw)

    def __parse_raw(self, raw):
        try:
            parsed = re.compile('(.*?)<(.*?)>').search(raw).groups()
            name = parsed[0].strip().strip('"')
            address = parsed[1]
        except:
            name, address = None, None
        self.Name = name
        self.Address = address

    def __repr__(self):
        return u"{0} <{1}>".format(self.Name, self.Address)

    def __str__(self):
        return u"{0} <{1}>".format(self.Name, self.Address)


class Gmail():
    def __init__(self, credentials_file='client_secret.json'):
        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/gmail-python-quickstart.json
        self.__scope = 'https://www.googleapis.com/auth/gmail.readonly'
        self.__clientSecretFile = credentials_file
        self.__applicationName = 'Gmail API Python'
        self.__credentials = None
        self.__setup()

    def __setup(self):
        self.__credentials = self.__get_credentials()
        http = self.__credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=http)

    def __get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(
            credential_dir, 'gmail-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                self.__clientSecretFile, self.__scope)
            flow.user_agent = self.__applicationName
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
    from apiclient import errors

    def search_messages(self, query=''):
        """List all Messages of the user's mailbox matching the query.

        Args:
          query: String used to filter messages returned.
          Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

        Returns:
          List of Messages that match the criteria of the query. Note that the
          returned list contains Message IDs, you must use get with the
          appropriate ID to get the details of a Message.
        """
        try:
            response = self.service.users().messages().list(userId='me', q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(
                    userId='me', q=query, pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except errors.HttpError, error:
            print 'An error occurred: %s' % error

    def get_raw_message(self, msg_id):
        """Get a Message with given ID.

        Args:
        msg_id: The ID of the Message required.

        Returns:
        A Message.
        """
        try:
            message = self.service.users().messages().get(userId='me', id=msg_id).execute()

            # print 'Message snippet: %s' % message['snippet']
            return message
        except errors.HttpError, error:
            print 'An error occurred: %s' % error

    def parse_message(self, msg):
        person_fields = ['To', 'From', 'Cc']
        date_fields = ['Date']
        text_fields = ['Subject']
        headers = msg['payload']['headers']

        message = {k: None for k in person_fields + date_fields + text_fields}
        for item in headers:
            header_field = item['name']
            if header_field in person_fields:
                people = item['value'].split(',')
                if len(people) == 1:
                    message[header_field] = Person(people[0])
                else:
                    message[header_field] = [Person(p) for p in people]
            elif header_field in date_fields:
                date = item['value']
                message[header_field] = date_parse(date)
            elif header_field in text_fields:
                text = item['value']
                message[header_field] = text
        return message

    def get_message(self, msg_id):
        """ Parse a message and get a dict of values
        Args:
            msg_id: The ID of the Message required.
        Returns:
            message dict
        """

        raw_message = self.get_raw_message(msg_id)
        return Message(raw_message)


if __name__ == "__main__":
    print "inmain"
    # try:
    #     with open('raw_message.pickle', 'rb') as f:
    #         # The protocol version used is detected automatically, so we do not
    #         # have to specify it.
    #         raw_message = pickle.load(f)
    # except:
    G = Gmail()
    test = G.search_messages('subject: "Re: Portland"')
    raw_message = G.get_raw_message(test[2]['id'])
    with open('raw_message.pickle', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(raw_message, f, pickle.HIGHEST_PROTOCOL)

    msg = Message(raw_message)
    # print msg
