from .client import Client, ready

import pprint
from collections import OrderedDict

RUN_KEYS = ['status',
            'next_frame',
            'run_label',
            'file_root',
            'directory',
            'start_frame',
            'axis_motor',
            'start_angle',
            'end_angle',
            'delta',
            'wedge_size',
            'exposure_time',
            'distance',
            'beam_stop',
            'attenuation',
            'num_energy',
            'energy1',
            'energy2',
            'energy3',
            'energy4',
            'energy5',
            'detector_mode',
            'inverse_on']

RUN_KEY_ALIAS = {'prefix': 'file_root', 'energy': 'energy1'}


class Runs(Client):
    def __init__(self, *args, **kwargs):
        super(Runs, self).__init__(*args, **kwargs)

        self.runs = {}

    def _process_message(self, msg):
        super(Runs, self)._process_message(msg)

        if (msg.startswith('stog_set_string_completed run') or
            msg.startswith('stog_configure_string run')):

            string_name, data = msg.split(None, 2)[1:]
            data = data.split()[1:]  # remove self
            if string_name == 'runs':
                self.runs[string_name] = data

            try:
                run_no = int(string_name[3:])  # noqa Needed?
                self.runs[string_name] = OrderedDict(zip(RUN_KEYS, data))
            except ValueError:
                pass

    def add_run(self):
        self.run_operation('runsConfig', self.user, 'addNewRun')

    def delete_run(self, run_no):
        run_no = int(run_no)
        self.run_operation('runsConfig', self.user, 'deleteRun', run_no)

    def reset_run(self, run_no):
        self.run_operation('runsConfig', self.user, 'resetRun', run_no)

    def reset_all(self):
        # resetAllRuns command fails
        # so we will just loop and do all manually
        for i in range(17):
            self.reset_run(i)

    def hide_all(self):
        self.show_runs(0)

    @ready
    def show_if_hidden(self, run_no):
        if int(self.runs['runs'][0]) < int(run_no):
            self.show_runs(run_no)

    @ready
    def show_runs(self, run_no):
        runs_settings = self.runs['runs']
        runs_settings[0] = str(run_no)
        runs_settings[1] = str(run_no)

        self.set_string('runs', " ".join(runs_settings))

    @ready
    def set_run(self, run_id, **kwargs):
        current = self.runs[run_id]
        for key, value in kwargs.iteritems():
            if value is None:
                continue
            if key in RUN_KEYS:
                current[key] = str(value)
            if key in RUN_KEY_ALIAS:
                current[RUN_KEY_ALIAS[key]] = str(value)

        self.set_string(run_id, " ".join(current.values()))

    @ready
    def start_run(self, run_no, **kwargs):
        self.run_operation('collectRun', run_no, self.user, 0,
                           'PRIVATEXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    @ready
    def print_runs(self):
        pprint.pprint(self.runs)

    @ready
    def return_runs(self):
        return self.runs

    @ready
    def get_active_run(self):
        for run_str, data in self.runs.iteritems():
            if run_str == 'runs':
                continue
            if data.get('status') == 'active':
                break
        else:
            raise Exception('No active run')
        return data
