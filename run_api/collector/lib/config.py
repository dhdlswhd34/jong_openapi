root = '/data'

class OpenApi:
    key = 's3Jp4uhVUQKAEvI1uIsRrRyNC9isNrQv69cKmvXdXyNpYk8AZ9xzrrUbKSZTO28TURJGfJla5CgyPmCl06AP%2BA%3D%3D'

class LH_Api:
    key = 'WImruyXsZ0iBn%2Bc1ZAB4oFgVpC8jU%2B%2Bspz4rAazLaglvajSPSWgPMxNQet72x79u6JUOqYp2SWlR5fhZPh6egQ%3D%3D'

class LH_web:
    URL = 'https://ebid.lh.or.kr/ebid.et.tp.cmd.BidsrvcsDetailListCmd.dev?bidNum='
    

class LH_web_result:
    URL = 'https://ebid.lh.or.kr/ebid.et.tp.cmd.TenderOpenDetailCmd.dev?bidNum='


class DBConfig:
    host = 'localhost'
    port = '5432'
    dbname = 'jong'
    user = 'jong'
    password = 'jong!'

class PathConfig:
    apps = f'{root}/apps'
    files = f'{root}/data'
    logs = f'{root}/logs'
    tmp = f'{root}/tmp'
    file_raw_date = f'{root}/apps/processing/.raw_date'
    file_last_date = f'{root}/apps/processing/.file_date'

class DocuxConfig:
    docux = f'{root}/pkg/docux/docux'
    tmp = f'{root}/tmp'
    max_length = 10 * 1024 * 1024

class LoggerConfig:
    path = f'{root}'

class ESConfig:
    host = 'localhost'
    port = '19200'
    timeout = 60
    max_retries = 5
    retry_on_timeout = True
    read_timeout = '120s'
