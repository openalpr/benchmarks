#!/usr/bin/python

from openalpr import Alpr
import os
import threading
import time
import sys
from argparse import ArgumentParser
import json
import yaml
from shapely.geometry import Polygon
from prettytable import PrettyTable

reload(sys)
sys.setdefaultencoding('utf-8')

parser = ArgumentParser(description='End to End Benchmark')

parser.add_argument(  "folder", action="store", type=str, 
                  help="Folder to benchmark" )

parser.add_argument( "-c", "--country", dest="country", action="store", type=str, required=True, 
                  help="Country to use for processing" )

parser.add_argument( "-j", "--json_export_file", dest="json_export_file", action="store", type=str, default=None, 
                  help="Export to JSON file" )

parser.add_argument( "--threads", dest="threads", action="store", type=int, required=False, default=8,
                  help="Total # of simmultaneous processes" )

options = parser.parse_args()

if not os.path.isdir(options.folder):
    print "Folder does not exist"
    sys.exit(1)

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def is_overlapping(plate_corners_gt, plate_coordinates):
    gt_points = []
    for p in plate_corners_gt.split():
        gt_points.append(int(p))

    p1_points = []
    for i in range(0, len(gt_points), 2):
        p1_points.append((gt_points[i], gt_points[i+1]))


    p2_points = []
    for i in range(0, 4):
        p2_points.append((plate_coordinates[i]['x'], plate_coordinates[i]['y']))

    p1 = Polygon(p1_points)
    p2 = Polygon(p2_points)

    intersection = p1.intersection(p2)
    union = p1.union(p2)

    i_over_u = intersection.area / union.area

    #print "I over U: " + str(i_over_u)
    return i_over_u > 0.4

def get_table_char(value):
    if value == True:
        return ""
    else:
        return "x"



class BenchStats():
    def __init__(self, plates_to_process):
        # Plates to process is a list of items from the yaml
        self.plates_to_process = plates_to_process
        self.images = {}
        for p in self.plates_to_process:
            img = p['image_file']

            if img not in self.images:
                self.images[img] = []
            
            self.images[img].append(p) 

        self.results = {}

    def add_result(self, image_file, result):
        
        detected = False
        correct_state = False
        top_n_match = False
        match_with_pattern = False
        top_1_match = False
        plate_number_gt = ""
        has_state = False
        #print "ADDED RESULT"
        #print json.dumps(result, indent=2)


        for gt in self.images[image_file]:
            overlap = is_overlapping(gt['plate_corners_gt'], result['coordinates'])

            plate_number_gt = str(gt['plate_number_gt']).decode("utf-8")
            plate_number_machine = str(result['candidates'][0]['plate']).decode("utf-8")


            if overlap:

                detected = True
                if 'region_code_gt' in gt:
                    has_state = True
                    correct_state = result['region'] == gt['region_code_gt'] or result['region'] == options.country + "-" + str(gt['region_code_gt'])
                    # Check if top match with state is right
                    for candidate in result['candidates']:
                        candidate_str = str(candidate['plate']).decode("utf-8")
                        if candidate['matches_template'] > 0:
                            match_with_pattern = candidate_str == plate_number_gt
                            break


                # print result
                top_1_match = plate_number_machine == plate_number_gt
                # print "%s == %s " % (result['plate'], plate_number_gt) + str(top_1_match)
                for candidate in result['candidates']:
                    top_n_match = candidate['plate'] == plate_number_gt
                    if top_n_match:
                        break

                if not match_with_pattern:
                    match_with_pattern = top_1_match

                break
 
        #print "top_1_match: " + str(top_1_match)

        if image_file not in self.results:
            self.results[image_file] = []

        json_data = {
            'image': image_file,
            'best_result': plate_number_machine,
            'detected': detected,
            'has_state': has_state,
            'correct_state': correct_state,
            'top_n_match': top_n_match,
            'match_with_pattern': match_with_pattern,
            'top_1_match': top_1_match,
            'plate_number_gt': None
        }

        if overlap:
            json_data['plate_number_gt'] = plate_number_gt

        self.results[image_file].append(json_data)

        return json_data


    def get_actual_result(self, image, plate_number_gt):
        if image not in self.results:
            return None
        for result in self.results[image]:
            if str(result['plate_number_gt']).decode("utf-8") == str(plate_number_gt).decode("utf-8"):
                return result

    def print_results(self):

        count_detected = 0
        count_top_n = 0
        count_top_pattern = 0
        count_top_1 = 0
        count_state_total = 0
        count_state = 0

        false_detections = 0

        data_rows = []
        falsep_rows = []

        # Print the positive scores
        tbl = PrettyTable()
        tbl.field_names = ["Image", "Yaml", "Detected", "Top N", "Top Match with Pattern", "Top 1", "State Match", "Best result", "Ground Truth"]
        tbl.align["Image"] = "l"
        for plate in plates_to_process:
            machine_result = self.get_actual_result(plate['image_file'], plate['plate_number_gt'])
            
            print str(machine_result)
            if machine_result is None:

                row =  {
                    'image_file': plate['image_file'], 
                    'yaml_file': plate['yaml_file'], 
                    'detected': False, 
                    'top_n_match': False, 
                    'match_with_pattern': False, 
                    'top_1_match': False, 
                    'has_state': True,
                    'correct_state': False,
                    'best_result': "",
                    'plate_number_gt': plate['plate_number_gt']
                        }

            else:


                row =  {
                    'image_file': plate['image_file'], 
                    'yaml_file': plate['yaml_file'], 
                    'detected': machine_result['detected'], 
                    'top_n_match': machine_result['top_n_match'], 
                    'match_with_pattern': machine_result['match_with_pattern'], 
                    'top_1_match': machine_result['top_1_match'], 
                    'has_state': machine_result['has_state'],
                    'correct_state': machine_result['correct_state'],
                    'best_result': machine_result['best_result'],
                    'plate_number_gt': plate['plate_number_gt']
                        }


                if machine_result['has_state']:
                    count_state_total += 1
                if machine_result['detected']:
                    count_detected += 1
                if machine_result['top_n_match']:
                    count_top_n += 1
                if machine_result['match_with_pattern']:
                    count_top_pattern += 1
                if machine_result['top_1_match']:
                    count_top_1 += 1
                if machine_result['correct_state']:
                    count_state += 1


            data_rows.append(row)
            state_val = '-'
            if row['has_state']:
                state_val = get_table_char(row['correct_state'])

            tbl.add_row([
                row['image_file'], 
                row['yaml_file'], 
                get_table_char(row['detected']), 
                get_table_char(row['top_n_match']), 
                get_table_char(row['match_with_pattern']), 
                get_table_char(row['top_1_match']), 
                state_val,
                row['best_result'],
                row['plate_number_gt']
                    ])

        print ""
        print "True Positives"
        print(tbl)

        # Print the negative scores:


        tbl = PrettyTable()
        tbl.field_names = ["Image", "False Detection", "Plate Number"]
        tbl.align["Image"] = "l"
        for image, values in self.results.iteritems():
            for value in values:
                if value['detected'] == False:
                    false_detections += 1
                    tbl.add_row([value['image'], "True", value['best_result']])
                    falsep_rows.append({'image_file': value['image'], 'best_result': value['best_result']})

        print ""
        print "False positives"
        print(tbl)

        def print_percent(name, count, total):
            if total == 0:
                percent = 0
            else:
                percent = float(count) /    float(total) * 100.0
            percent_str = "%.2f" % (percent)

            disp_name = name + ":"
            print disp_name.ljust(20) + str(count).ljust(4) + " / " + str(total).ljust(4) + ": " + percent_str.rjust(4) + "%"

        total_plates = len(self.plates_to_process)
        print_percent("Detected", count_detected, total_plates)
        print_percent("Top N", count_top_n, total_plates)
        print_percent("Top Pattern", count_top_pattern, total_plates)
        print_percent("Top 1", count_top_1, total_plates)
        print_percent("State Match", count_state, count_state_total)
        print ""
        print_percent("False Positives", false_detections, total_plates)

        if options.json_export_file is not None:

            data = {
                'detected': count_detected,
                'top_n': count_top_n,
                'top_pattern': count_top_pattern,
                'top_1': count_top_1,
                'state_match': count_state,
                'total': total_plates,
                'total_state': count_state_total,
                'false_positives': false_detections,
                'rows': data_rows,
                'false_positive_rows': falsep_rows
            }
            with open(options.json_export_file, 'w') as jsonout:
                json.dump(data, jsonout)


processing_thread_status = []
for i in range (0,options.threads):
    processing_thread_status.append(1)

threadLock = threading.Lock()
class PlateProcessorThread (threading.Thread):

    def __init__(self, metadata, thread_number=0, total_threads=1):
        global processing_threads
        threading.Thread.__init__(self)
        self.metadata = metadata
        self.thread_number = thread_number
        self.total_threads = total_threads
        self.complete = False

    def run(self):
        global processing_threads

        bench_config = os.path.join(SCRIPT_DIR, "config/bench.conf")
        self.alpr = Alpr(options.country, bench_config, "/usr/share/openalpr/runtime_data/")

        print("Initiating thread #%d" % (self.thread_number))

        counter = 0
        for plate in self.metadata:
            image_path = os.path.join(options.folder, plate['image_file'])

            if counter % self.total_threads != self.thread_number:
                # Skip this because another thread is processing it
                counter += 1
                continue

            counter += 1
            if self.thread_number == 0:
                print "Processing %d / %d" % (counter, len(self.metadata))

            if not os.path.isfile(image_path):
                print "Could not find: %s" % (image_path)
                sys.exit(1)

            results = self.alpr.recognize_file(image_path)
            
            # print json.dumps(results, indent=2)

            threadLock.acquire()
            for result in results['results']:
                benchstats.add_result(plate['image_file'], result)
            threadLock.release()

        threadLock.acquire()
        processing_thread_status[self.thread_number] = 0
        threadLock.release()
        self.complete = True

        print "Thread %d complete" % (self.thread_number)

plates_to_process = []
for file in os.listdir(options.folder):
    full_path = os.path.join(options.folder, file)

    if file.endswith('.yaml'):
        with open(full_path, 'r') as yi:
            data = yaml.load(yi)
            data['yaml_file'] = file
            #print json.dumps(data, indent=2)

            plates_to_process.append(data)


benchstats = BenchStats(plates_to_process)


threads = []
for i in range(0, options.threads):

    t = PlateProcessorThread(plates_to_process, i, options.threads)
    t.daemon = True
    t.start()
    threads.append(t)


# Wait for all worker processes to finish


while True:
    completion_count = 0
    for i in range(0, len(threads)):
        threads[i].join(0.1)
        if threads[i].isAlive():
            completion_count = 0
        else:
            completion_count += 1

    if completion_count == len(threads):
        break




benchstats.print_results()
