import datetime as dt


def year(request):
    year_ = dt.datetime.now().year
    return {"year": year_}
