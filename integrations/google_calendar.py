import requests


def create_google_calendar_event(access_token, meeting):

    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    event_data = {
        "summary": meeting.title,
        "description": meeting.description,
        "start": {
            "dateTime": meeting.start_time.isoformat(),
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": meeting.end_time.isoformat(),
            "timeZone": "UTC",
        },
    }

    response = requests.post(url, headers=headers, json=event_data)

    if response.status_code != 200:
        raise Exception(f"Google Calendar API error: {response.text}")

    return response.json().get("id")