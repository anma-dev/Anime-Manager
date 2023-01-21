
class CBreaker():
    '''
    Circuit breaker logic for nyaa.si http requests.\n
    It prevents further network requests to nyaa in the \n
    event of a long-lasting transient fault. Part of \n
    Anime Manager.
    https://github.com/anma-dev/Anime-Manager
    '''

    def __init__(self):
        self.OPEN = 0
        self.HALF_CLOSED = 1
        self.CLOSED = 2
        self.status = self.CLOSED

    def open(self):
        '''
        Set the circuit breaker as open to signal a long-lasting service fault.
        '''
        self.status = self.OPEN

    def close(self):
        '''
        Close the circuit breaker to disable it.
        '''
        self.status = self.CLOSED

    def half_open(self):
        '''
        Set the circuit breaker as half-open to signal an available retry window.
        '''
        self.status = self.HALF_CLOSED

    def get_status(self):
        '''
        Get the circuit breaker status.
        '''
        return self.status
