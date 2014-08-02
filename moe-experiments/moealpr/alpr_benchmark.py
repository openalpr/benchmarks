'''
Runs the benchmark that MOE needs.
Given a list of settings, ALPR gets updated, and the benchmark is run.
It returns a single quality metric.
'''

import re
from subprocess import call
import os

class AlprBenchmark:
    def __init__(self):
        pass

    '''
    Executes the benchmark test and returns a single percent score between 0 and 100
    '''
    def execute(self):
        pass

class AlprEndToEndBenchmark(AlprBenchmark):

    def execute(self):
        benchmark_program = '/storage/projects/alpr/src/build/misc_utilities/benchmark'
        country = 'us'
        benchmark = 'endtoend'
        plate_dir = '/storage/projects/alpr/benchmarks/endtoend/us/'
        output_results = '/tmp/'
        summary_file = 'summary.txt'

        devnull = open(os.devnull, 'w')
        call([benchmark_program, country, benchmark, plate_dir, output_results], stdout=devnull)
        devnull.close()

        return self._getResult(output_results + summary_file)

    def _getResult(self, summary_file):

        if not os.path.isfile(summary_file):
            return 0

        # Skip first 7 lines for EXACT match
        # Skip first 6 lines for TOP10 match
        inputfile = open(summary_file)
        lines = inputfile.readlines()
        inputfile.close()

        pattern = re.compile("[0-9]+\.*[0-9]*$")
        top10line = lines[6]
        exactline = lines[7]

        top10 = float(pattern.search(top10line).group(0))
        exact = float(pattern.search(exactline).group(0))

        # Delete the file
        os.remove(summary_file)

        return (top10 + exact) / 2

