import datetime

class ClockEvent(object):
    CLOCK_IN = 0
    CLOCK_OUT = 1
    CLOCK_TIME = 2
    def __init__(self, event_type, duration=None):
        if event_type not in (ClockEvent.CLOCK_IN, ClockEvent.CLOCK_OUT, ClockEvent.CLOCK_TIME):
            raise ValueError("Invalid event type. Must be one of CLOCK_IN, CLOCK_OUT, CLOCK_TIME")
        self.start_time = datetime.datetime.now()
        self.end_time = datetime.datetime.now()
        self.event_type = event_type
    @property
    def time(self):
        return self.start_time

def compute_time(clock_events):
    if not clock_events:
        return datetime.timedelta()
    clocked_in = False
    total_time = datetime.timedelta()
    for event in clock_events:
        if event.event_type == ClockEvent.CLOCK_IN:
            clocked_in = True
            last_time = event.time
        elif event.event_type == ClockEvent.CLOCK_OUT:
            if clocked_in:
                total_time += (event.time - last_time)
                last_time = event.time
            clocked_in = False
        elif event.event_type == ClockEvent.CLOCK_TIME:
            total_time += event.duration

    if clocked_in:
        total_time += (datetime.datetime.now() - last_time)
    return total_time

