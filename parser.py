import csv
import re


# function to calculate latency
def latency(ts_PTT_list, ts_playString_list):
    latency_list = []
    for (ts_PTT, ts_playString) in zip(ts_PTT_list, ts_playString_list):
        latency = ts_playString - ts_PTT + 600
        latency_list.append(latency)
    print latency_list
    return latency_list


# function to pick timestamp from log and convert it to integer
def stripper(timestamp_list):
    response_timestamp = 0
    regexp = "[^\n]\d\d\d\d\d\d\d\d\d\d"
    for playstring in timestamp_list:
        stripped_list = re.findall(regexp, playstring)  # picks only timestamps from the log line
        for tss in stripped_list:
            response_timestamp = int(tss.replace('_', ''))
    return response_timestamp


# function to get unique values
def unique(timestamp_list):
    # insert the list to the set
    list_set = set(timestamp_list)
    unique_list = (list(list_set))  # removes duplicate entries from list
    response_timestamp = stripper(unique_list)
    return response_timestamp


# function to generate csv file
def write_csv(latency_list):
    min_latency = min(latency_list)
    max_latency = max(latency_list)
    average_latency = sum(latency_list) / len(latency_list)
    attempts_count = len(latency_list)
    utterance = 'Number 2'  # TODO: Enter correct command
    with open('output.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        header = ['Utterance', 'No. of attempts', 'AVG(ms)', 'MIN(ms)', 'MAX(ms)']
        writer.writerow(header)
        writer.writerow(
            (utterance, attempts_count, average_latency, min_latency, max_latency))


# function to open log file and perform parsing
def log_reader(filename, target_name):
    with open(filename) as f:
        log = f.read()
        if target_name.lower() == 'dten':
            block_regex = "EVNT GDM NAME=PTT hmi_active_screen=HMI_ACTIVE_NONE[\w\W]*?Scheduled event after flush: N"
        else:
            block_regex = "EVNT GDM NAME=PTT hmi_active_screen='HMI_ACTIVE_NONE'[\w\W]*?Scheduled event after flush: N"

        # Dten
        # block_regex = "EVNT GDM NAME=PTT hmi_active_screen=HMI_ACTIVE_NONE[\w\W]*?Scheduled event after flush: N"
        # PANASONIC
        # block_regex = "EVNT GDM NAME=PTT hmi_active_screen='HMI_ACTIVE_NONE'[\w\W]*?Scheduled event after flush: N"

        regex_PTT = ".*beginSpeechFrame"
        regex_playString = "(.*nuance_prompter_IPrompter_playString IPrompter_instance='SDS_prompter' " \
                           "IPrompt_instance='IPrompt_)(?!.*wav.*)"
        ts_PTT_list = []
        ts_playString_list = []
        result = re.findall(block_regex, log)
        for block in result:
            list_PTT = []
            list_PTT.append(re.findall(regex_PTT, block)[-1])
            ts_PTT = unique(list_PTT)
            ts_PTT_list.append(ts_PTT)
            print 'ts_PTT: ', ts_PTT
            list_Play = []
            list_Play.append(re.findall(regex_playString, block)[-1])
            ts_playString = unique(list_Play)
            ts_playString_list.append(ts_playString)
            print 'ts_playString', ts_playString

    print ts_PTT_list
    print ts_playString_list
    latency_list = latency(ts_PTT_list, ts_playString_list)
    write_csv(latency_list)


# main function
if __name__ == '__main__':
    target_name = 'pan'  # TODO: Enter either dten or pan
    log_reader('log', target_name)
