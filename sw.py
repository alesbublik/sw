#!/usr/bin/env python

from opterator import opterate

import csv
import sys

UP = 'UP'
DOWN = 'DOWN'
UNCONFIRMED_DOWN = 'UNCONFIRMED_DOWN'
STATUS_LIST = (UP, DOWN, UNCONFIRMED_DOWN)

CHECK_IDS = {}

def parse_line(line):
    values = line.strip().split(',')
    dict_values = {'time': int(values[0]),
                   'check': int(values[1]),
                   'resp_time': int(values[2]),
                   'status': values[3]}
    return dict_values

def print_consumer():
    while True:
        value = (yield)
        print(value)

def check_state_machine():
    # initialize state machine
    values = (yield)
    status_list = []
    current_state = {'start_time': values['time'],
                     'end_time' : '',
                     'status': values['status']}
    while True:
        # then wait for data
        values = (yield)
        if values == 'finish':
            yield (status_list + [current_state])

        if values['status'] == UNCONFIRMED_DOWN:
            unconfirmed_time = values['time']
        elif values['status'] != current_state['status']:
            if unconfirmed_time:
                start_time = unconfirmed_time
            else:
                start_time = values['time']
            current_state['end_time'] = start_time
            status_list.append(current_state)
            current_state = {'start_time': start_time,
                             'end_time' : values['time'],
                             'status': values['status']}
            unconfirmed_time = None
        else:
            current_state['end_time'] = values['time']



def sw_state_machine(consumers):
    while True:
        values = (yield)
        check_id = values['check']
        if check_id not in CHECK_IDS:
            check_machine = check_state_machine()
            next(check_machine)
            CHECK_IDS[check_id] = check_machine

        check = CHECK_IDS[check_id]
        check.send(values)

        [consumer.send(values) for consumer in consumers]


def reduce_status():
    check_id_list = CHECK_IDS.keys()
    check_id_list.sort()

    field_names = ['checkid', 'start_time', 'end_time', 'status']
    csv_writer = csv.DictWriter(sys.stdout, fieldnames=field_names, delimiter=',')
    csv_writer.writeheader()

    for check_id in check_id_list:
        check = CHECK_IDS[check_id]
        res = check.send('finish')
        for row in res:
            row['checkid'] = check_id
            csv_writer.writerow(row)


@opterate
def main(source_filename):
    """
    Script for processing checks
    :param source_filename: checks source filename
    """
    with open(source_filename, 'rt') as f:
        consumer = print_consumer()
        next(consumer)

        state_machine = sw_state_machine([])
        next(state_machine)

        for line in f:
            values = parse_line(line)
            status = values['status']
            if status not in STATUS_LIST:
                # raise exception or log
                continue

            state_machine.send(values)

        reduce_status()

if __name__ == '__main__':
    main()
