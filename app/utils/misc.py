
from datetime import datetime

day_to_query = datetime.today().strftime('%Y-%m-%d')
from_date_str = day_to_query + "T00:00:00+00:00"
to_date_str = day_to_query + "T23:59:59+00:00"
from_date = datetime.strptime(from_date_str, '%Y-%m-%dT%H:%M:%S%z')
to_date = datetime.strptime(to_date_str, '%Y-%m-%dT%H:%M:%S%z')
