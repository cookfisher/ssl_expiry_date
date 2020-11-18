# Author: Jia Ming Wei
# modified from https://github.com/LucasRoesler/ssl-expiry-check/blob/master/ssl_expiry.py

import datetime
import logging
import os
import socket
import ssl
import time
from colorama import Fore, Style

logger = logging.getLogger('SSLVerify')

def ssl_expiry_datetime(hostname: str) -> datetime.datetime:
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    conn.settimeout(3.0)

    logger.debug('Connect to {}'.format(hostname))
    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)

def check_host(hostname: str, buffer_days: int=30) -> str:
    try:
        """Get an expiry date"""
        expiry_date = ssl_expiry_datetime(hostname)
        print(f'{hostname} SSL certificate expiry date is ' + expiry_date.strftime("%m/%d/%Y, %H:%M:%S"))
        """Get ssl remaining valid time"""
        remain_time = expiry_date - datetime.datetime.utcnow()
    except ssl.CertificateError as e:
        return f'{hostname} certificate error {e}'
    except ssl.SSLError as e:
        return f'{hostname} certificate error {e}'
    except socket.timeout as e:
        return f'{hostname} could not connect'
    else:
        if remain_time < datetime.timedelta(days=15):
            return Fore.RED + 'CRITICAL' + Style.RESET_ALL + f' {hostname} certificate will expire within next 15 days'
        elif remain_time < datetime.timedelta(days=30):
            return Fore.YELLOW + 'WARNING' + Style.RESET_ALL +f' {hostname} certificate will expire within next 30 days '
        else:
            return Fore.GREEN + 'INFO'+ Style.RESET_ALL + f' {hostname} certificate is fine'

if __name__ == '__main__':
    loglevel = os.environ.get('LOGLEVEL', 'INFO')
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level)
    start = time.time()

    """Replace 'your_hostname' with your actually hostname, like 'server01'"""
    host = 'your_hostname'
    message = check_host(host)
    print(message)

    print('\n')

    """Replace 'your_url' with your target remote server's url or ip address, like 'example.com'"""
    host = 'your_url'
    message = check_host(host)
    print(message)

    logger.debug('Time: {}'.format(time.time() - start))
