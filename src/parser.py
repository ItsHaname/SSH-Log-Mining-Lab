"""Parse SSH authentication logs and turn them into transactions.

A transaction is the set of items describing one authentication event, e.g.
    {'event=failed_password', 'user=root', 'ip=45.83.12.9',
     'auth=password', 'period=night', 'status=failure'}
"""

import re

# Syslog prefix: "Sep 16 01:18:38 raspberrypi sshd[1213]: <message>"
# OpenSSH >= 9.8 logs from "sshd-session" instead of "sshd", so both are accepted.
LINE_RE = re.compile(
    r"^(?P<month>\w{3})\s+(?P<day>\d{1,2})\s"
    r"(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})\s"
    r"(?P<host>\S+)\s+sshd(?:-session|-auth)?\[(?P<pid>\d+)\]:\s(?P<message>.*)$"
)

# Message patterns, tried in order. Each one yields (event, auth, status).
MESSAGE_RES = [
    (
        re.compile(r"^Failed (?P<auth>password|publickey) for invalid user "
                   r"(?P<user>\S+) from (?P<ip>\S+) port \d+"),
        "failed_invalid_user", "failure",
    ),
    (
        re.compile(r"^Failed (?P<auth>password|publickey) for "
                   r"(?P<user>\S+) from (?P<ip>\S+) port \d+"),
        "failed_password", "failure",
    ),
    (
        re.compile(r"^Accepted (?P<auth>password|publickey) for "
                   r"(?P<user>\S+) from (?P<ip>\S+) port \d+"),
        "accepted", "success",
    ),
    (
        re.compile(r"^Invalid user (?P<user>\S+) from (?P<ip>\S+) port \d+"),
        "invalid_user", "failure",
    ),
    (
        re.compile(r"^Connection closed by authenticating user "
                   r"(?P<user>\S+) (?P<ip>\S+) port \d+"),
        "connection_closed", "failure",
    ),
    (
        re.compile(r"^Disconnected from invalid user "
                   r"(?P<user>\S+) (?P<ip>\S+) port \d+"),
        "disconnected", "failure",
    ),
]


def period_of_day(hour):
    """Group an hour into a coarse time slot."""
    if 0 <= hour < 6:
        return "night"
    if 6 <= hour < 12:
        return "morning"
    if 12 <= hour < 18:
        return "afternoon"
    return "evening"


def parse_line(line):
    """Parse one log line into an event dict, or return None if unrecognised."""
    head = LINE_RE.match(line)
    if not head:
        return None

    message = head.group("message")
    for pattern, event, status in MESSAGE_RES:
        found = pattern.match(message)
        if not found:
            continue
        fields = found.groupdict()
        hour = int(head.group("hour"))
        return {
            "month": head.group("month"),
            "day": int(head.group("day")),
            "time": f"{head.group('hour')}:{head.group('minute')}:{head.group('second')}",
            "hour": hour,
            "period": period_of_day(hour),
            "host": head.group("host"),
            "pid": int(head.group("pid")),
            "event": event,
            "status": status,
            "user": fields.get("user"),
            "ip": fields.get("ip"),
            "auth": fields.get("auth"),
        }
    return None


def parse_file(path):
    """Parse a log file and return the list of recognised SSH events."""
    events = []
    with open(path, "r", errors="replace") as handle:
        for line in handle:
            event = parse_line(line.rstrip("\n"))
            if event:
                events.append(event)
    return events


def event_to_transaction(event):
    """Turn one event into a sorted list of items."""
    items = [
        f"event={event['event']}",
        f"status={event['status']}",
        f"period={event['period']}",
        f"user={event['user']}",
        f"ip={event['ip']}",
    ]
    if event["auth"]:
        items.append(f"auth={event['auth']}")
    return sorted(items)


def to_transactions(events):
    """Turn a list of events into a list of transactions."""
    return [event_to_transaction(event) for event in events]


def load_transactions(path):
    """Read a log file and return its transactions."""
    return to_transactions(parse_file(path))
