'''
An ALPR experiment runs in concert with MOE to find the optimal value for 'n' settings

Given a benchmark, and a list of settings, the ALPR experiment will communicate with MOE to manage
the next values to use.  It also keeps track of the results and stops it when the experiment is complete.
'''

import sys, time
from moe.easy_interface.experiment import Experiment
from moe.optimal_learning.python.data_containers import SamplePoint
import moe.easy_interface.simple_endpoint as simple_endpoint

class AlprExperiment:

    def __init__(self, benchmark, settings_list):
        # Run the experiment once to get the initial value

        self.benchmark = benchmark
        self.settings = settings_list
        self.results = []

        self.iteration_count = 0

        bounds = []

        for setting in self.settings:
            bounds.append([setting.get_minimum(), setting.get_maximum()])

        self.moe = Experiment(bounds)


    def run(self, iterations):

        while self.iteration_count < iterations:
            print "Experiment iteration " + str(self.iteration_count + 1) + " of " + str(iterations)
            sys.stdout.flush()
            self._iterate()

            self.iteration_count = self.iteration_count + 1

        print "Experiment finished..."

        for setting in self.settings:
            setting.finish()

    '''
    Runs a single benchmark, feeds the results into MOE, and then updates the settings with new values
    '''
    def _iterate(self):

        result = self.benchmark.execute()

        inverted_result = 100-result

        self.moe.historical_data.append_sample_points([
            SamplePoint(self._getValues(), inverted_result, 0.1 )
        ])

        print "  -- Results: " + str(result)

        for setting in self.settings:
            print "    -- " + str(setting)

        self._getNextParamFromMOE()

        sys.stdout.flush()

    def _getNextParamFromMOE(self):

        while True:
            try:
                next_points_to_sample = simple_endpoint.gp_next_points(self.moe)[0]
                self._updateSettings(next_points_to_sample)
                break
            except:
                pass

            print "Error connecting to MOE.  Retrying..."
            time.sleep(2.0)

    def _getValues(self):
        value_array = []
        for setting in self.settings:
            value_array.append(setting.get_value())

        return value_array

    def _updateSettings(self, value_array):
        for i in range(0, len(value_array)):
            self.settings[i].set_value(value_array[i])

