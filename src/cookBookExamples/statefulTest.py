# this module is use for testing the section 8.19 stateful check.

class Connection:
    def __init__(self) -> None:
        self.newState(ClosedConnectionState)
    
    def newState(self, newState):
        self._state = newState

    def read(self):
        return self._state.read(self)

    def write(self,data):
        return self._state.write(self, data)

    def open(self):
        return self._state.open(self)

    def close(self):
        return self._state.close(self)

class ConnectionState:

    @staticmethod
    def read(conn):
        raise NotImplementedError()

    @staticmethod
    def write(conn, data):
        raise NotImplementedError()

    @staticmethod
    def open(conn):
        raise NotImplementedError()

    @staticmethod
    def close(conn):
        raise NotImplementedError()

class ClosedConnectionState(ConnectionState):

    @staticmethod
    def read(conn):
        raise RuntimeError('Not open')
    
    @staticmethod
    def wrute(conn, data):
        raise RuntimeError('Not open')

    @staticmethod
    def open(conn):
        conn.newState(OpenConnectionState)

    @staticmethod
    def close(conn):
        raise RuntimeError('Closd Already.')

class OpenConnectionState(ConnectionState):

    @staticmethod
    def read(conn):
        print('reading')

    @staticmethod
    def write(conn, data):
        print('write')

    @staticmethod
    def open(conn):
        raise RuntimeError('Opened Already.')

    @staticmethod
    def close(conn):
        conn.newState(ClosedConnectionState)

c = Connection()
print('Conection state:')
print(c._state)
try:
    c.read()
except Exception as e: 
    print(e)
c.open()
print(c._state)

c.write("test data")
c.close()







