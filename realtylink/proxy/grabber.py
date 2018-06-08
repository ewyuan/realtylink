"""
The following code is an adapted version of the proxybroker example.
https://proxybroker.readthedocs.io/en/latest/examples.html

Find 50 working HTTP(S) proxies and save them to a file.
"""

import asyncio
from proxybroker import Broker


async def save(proxies, filename):
    """Save proxies to a file."""
    with open(filename, 'w+') as f:
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            proto = 'https' if 'HTTPS' in proxy.types else 'http'
            row = '%s://%s:%d\n' % (proto, proxy.host, proxy.port)
            f.write(row)


def run():
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.find(types=[('HTTP', 'High'), ('HTTPS', 'High')], limit=50),
                           save(proxies, filename='proxy/out/unchecked-proxies.txt'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

if __name__ == "__main__":
    run()
