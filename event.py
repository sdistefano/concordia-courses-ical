import pytz, icalendar, datetime, calendar
from dateutil import parser
import re, html
WRITE_AS_UTC = True             #google calendar

TZ = pytz.timezone('America/Montreal')

regex = re.compile(r'([a-zA-Z]{2,4}) (.*) - (.*)')

class CourseEvent(object):
    def __init__(self, name, number, section, component, times, room, instructor, start_end):
        name = html.unescape(name)
        self.name = '{} ({}) - {}'.format(name, component, room)
        self.description = """
Number: {}
Section: {}
Instructor: {}
        """.format(number, section, instructor).strip()
        self.section = section
        days, startt, endt = regex.match(times).groups()
        start, end = [n.strip() for n in start_end.split('-')]
        self.start_time = parser.parse('{} {} EST'.format(startt, start))
        first_day = days[0:2].lower()
        while calendar.day_name[self.start_time.weekday()].lower()[0:2] != first_day :
            self.start_time += datetime.timedelta(days=1)

        self.end_time = parser.parse('{} {} EST'.format(endt, self.start_time.date().isoformat()))

        nclasses = 13 * len(days) / 2

        fdays = []
        for x in range(int(len(days) / 2)):
            fdays.append(days[x*2:x*2+2])

        self.repeat_rule = {'freq': 'weekly', 'count': 13, 'byday': fdays}

        if WRITE_AS_UTC:
            self.start_time = pytz.utc.normalize(self.start_time.astimezone(pytz.utc))

    def as_ical(self):
        event = icalendar.Event()
        event.add('summary', u'{} ({})'.format(self.name, self.section))
        event.add('dtstart', self.start_time)
        event.add('dtend', self.end_time)
        event.add('description', self.description)
        event.add('rrule', self.repeat_rule)

        return event
