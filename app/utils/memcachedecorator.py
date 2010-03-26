"""
@memoize('account:name=%s')
def get_account_by_name(name):
    return Account.all().filter('name =', name).get()

"""

import settings  # When using Django so as to skip the cache during testing.
from defaults import Defaults
import hashlib
import google.appengine.api.memcache as memcache
import logging

def memoize(keyformat, time=60):
    """Decorator to memoize functions using memcache."""
    def decorator(fxn):
        def wrapper(*args, **kwargs):
            key = keyformat % args[0:keyformat.count('%')]
            data = memcache.get(key)
            if data is not None:
                return data
            data = fxn(*args, **kwargs)
            memcache.set(key, data, time)
            return data
        return wrapper
    return decorator if not Defaults.isDevelopmentServer() else fxn

def memoize2(time=120):
    """Decorator to memoize functions using memcache."""
    def decorator(fxn):
        def wrapper(*args, **kwargs):
            m = hashlib.md5()
            m.update(str(args))
            m.update(str(kwargs))
            key = m.hexdigest()
            data = memcache.get(key)
            if data is not None:
                logging.debug('key: "%s", hit' % key)
                return data
            logging.debug('key: "%s", miss' % key)
            data = fxn(*args, **kwargs)
            memcache.set(key, data, time)
            return data
        return wrapper
    return decorator if not Defaults.isDevelopmentServer() else fxn