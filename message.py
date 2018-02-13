import base64
import re
from dateutil.parser import parse as date_parse


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


class Message():
    def __init__(self, msg=None):
        self.to = None
        self.from_ = None
        self.cc = None
        self.body = None
        self.subject = None
        self.date = None
        self.internalDate = 0
        self.snippet = None

        if msg is not None:
            self.header_parse(msg)

    def header_parse(self, msg):
        # add snippet and internalDate from message base (not headers)
        self.add_nonheader('snippet', msg)
        self.add_nonheader('internalDate', msg)

        # get headers and add them
        headers = msg['payload']['headers']
        for item in headers:
            self.process_field(item['name'], item['value'])

    def process_field(self, field, value):
        person_fields = ['To', 'From', 'Cc']
        date_fields = ['Date']
        text_fields = ['Subject']
        if field in person_fields:
            if field == "From":
                field = "from_"
            self.add_person(field.lower(), value)
        elif field in date_fields:
            self.add_date(field.lower(), value)
        elif field in text_fields:
            self.add_text(field.lower(), value)

    def add_nonheader(self, field, msg):
        self.add_text(field, msg[field])

    def add_text(self, field, text):
        # print field, text
        setattr(self, field, text)

    def add_date(self, field, date):
        setattr(self, field, date_parse(date))

    def add_person(self, field, person):
        people = person.split(',')
        existing = getattr(self, field)
        if existing is None:
            setattr(self, field, [Person(p) for p in people])
        else:
            setattr(self, field, existing.extend([Person(p) for p in people]))

    def __repr__(self):
        value_store = self.__dict__
        output = []
        for key in value_store:
            key = unicode(key, "utf-8", 'replace')
            value = value_store[key]
            if value is None:
                value = u'None'
            else:
                value = repr(value)
            output.append(u'{}: {}'.format(key, value))
        return u'\n'.join(output)

    def __str__(self):
        value_store = self.__dict__
        output = []
        for key in value_store:
            key = unicode(key, "utf-8", 'replace')
            value = value_store[key]
            if value is None:
                value = u'None'
            else:
                value = repr(value)
            output.append(u'{}: {}'.format(key, value))
        return u'\n'.join(output)

    def __base64_url_decode(inp):
        padding_factor = (4 - len(inp) % 4) % 4
        inp += "=" * padding_factor
        return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))
