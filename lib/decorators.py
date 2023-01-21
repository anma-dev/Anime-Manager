import functools
from time import sleep
import requests
import sys
import return_codes as codes
from Logger import Logger
from circuit_breaker import CBreaker

logger = Logger(debug=True, log_name="decorators").log

'''
Python decorator functions for Anime Manager.
https://github.com/anma-dev/Anime-Manager
'''


def exp_back_off(c_breaker: CBreaker, sleep_t=1):
    '''
    Exponential back-off for network requests,
    implemented as part of Anime Manager nyaa
    search requests logic. It also takes into
    account retry-after header value if it 
    conforms to our defined timeout 
    requirements. It also set the state of a
    circuit breaker.
    '''
    def sleep_retry_fun(func):
        if (c_breaker.get_status() == c_breaker.OPEN):
            logger.error("Circuit breaker is open. Discarding request.")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timeout = 15
            t_counter = 0
            delay_increase = 2
            wait_t = sleep_t
            while t_counter < timeout:
                try:
                    func(*args, **kwargs)
                    c_breaker.close()
                    return
                except requests.exceptions.HTTPError as err:
                    if ("retry-after" in err.response.headers):
                        remote_wait_time = int(
                            err.response.headers["retry-after"])
                        if (remote_wait_time <= timeout):
                            logger.info(
                                f"Received Retry-After header. Sleeping for {remote_wait_time} seconds.")
                            sleep(remote_wait_time)
                            t_counter += remote_wait_time
                        else:
                            # long-lasting transient fault
                            logger.error(
                                f"Retry-After value exceeded timeout: {remote_wait_time} seconds.")
                            c_breaker.open()
                            break
                    else:
                        # exponential back-off
                        logger.info(
                            f'Sleeping for {wait_t} seconds')
                        sleep(wait_t)
                        t_counter += wait_t
                        wait_t += delay_increase
            # request failure
            err_msg = f"Nyaa service is unavailable."
            logger.error(err_msg)
            raise Exception(err_msg)
        return wrapper
    return sleep_retry_fun
