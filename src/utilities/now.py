from datetime import datetime, timedelta, timezone

def get_now_date(days: int = 30) -> datetime:
    """ 
    Returns datetime for 'days' ago from now
    """
    return datetime.now() - timedelta(days=days)

def get_now_timezone_date() -> datetime:
    """ 
    Get current UTC datetime without timezone info"
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)