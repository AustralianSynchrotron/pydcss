# DCS Protocol:
# http://smb.slac.stanford.edu/research/developments/blu-ice/dcsAdmin4_1/node96.html
# gui client
from .dcss import DCSS


# small decorator to assure we are master before doing stuff
def master(func):
    def wrapper(self, *args, **kwargs):
        if not self.become_master():
            raise Exception('Unable to become master!')
        return func(self, *args, **kwargs)
    return wrapper


# make sure we have heard the full update before doing stuff
def ready(func):
    def wrapper(self, *args, **kwargs):
        while not self.ready:
            self.read_message()
        return func(self, *args, **kwargs)
    return wrapper


class Client(DCSS):
    def __init__(self, server, session_id):
        super(Client, self).__init__(server=server, port=14243)

        self.master = False
        self.ready = False
        self.client_id = None
        self.operation_no = 0

        # some vars for dcss
        self.SID = session_id
        self.user = 'blctl'
        # dont actually need these but dcss wants them
        self.host = 'who_cares'
        self.display = ':0.0'

    def login(self):
        msg, data = self.read_message()
        if msg != 'stoc_send_client_type':
            raise Exception('Unexpected message %s' % (msg, ))

        fmt = 'gtos_client_is_gui {0.user} {0.SID} {0.host} {0.display}'
        login_msg = fmt.format(self)
        self.send_xos1(login_msg)

        msg, data = self.read_message()
        msg = msg.split()
        if msg[0] != 'stog_login_complete':
            raise Exception('Login Failed: Unexpected message %s' % (msg, ))

        self.client_id = msg[1]

    def _process_message(self, msg):
        if msg == 'stog_become_master':
            self.master = True
        if msg == 'stog_other_master' or msg == 'stog_become_slave':
            self.master = False
        if msg == 'stog_dcss_end_update_all_device':
            self.ready = True

    def become_master(self, force=True):
        if self.master:
            return True

        force_str = 'force'
        if not force:
            force_str = 'noforce'
        self.send_xos3('gtos_become_master %s' % force_str)

        # we will process messages for a while to check for sucess
        for msg in self.process_messages():
            if msg == 'stog_become_master':
                return True
            if msg == 'stog_other_master' or msg == 'stog_become_slave':
                return False

    @master
    def run_operation(self, name, *args):
        args = ' '.join(map(str, args))
        fmt = 'gtos_start_operation {name} {client_id}.{operation_no} {args}'
        msg = fmt.format(name=name, client_id=self.client_id,
                         operation_no=self.operation_no, args=args)
        self.operation_no += 1
        self.send_xos3(msg)

        # wait for completion
        msg = self.process_until('stog_operation_completed %s' % name)
        return msg

    def set_string(self, string_name, data):
        self.send_xos3('gtos_set_string %s %s' % (string_name, data))

        # wait for completion
        self.process_until('stog_set_string_completed %s' % string_name)
