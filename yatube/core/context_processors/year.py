import datetime as dt


def year(request):
    now = int(dt.datetime.now().year)
    return {
        'year': now
    }
