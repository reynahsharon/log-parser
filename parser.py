import csv
import re


# function to open log file and perform parsing
def reader(filename):
    with open(filename) as f:
        log = f.read()
        regex_PTT = ".*beginSpeechFrame"

        list_PTT = []
        list_PTT.append(re.findall(regex_PTT, log)[-1])
        ts_PTT = unique(list_PTT)  # finds the last final ASR result timestamp

        regex_playString = "(.*nuance_prompter_IPrompter_playString IPrompter_instance='SDS_prompter' " \
                           "IPrompt_instance='IPrompt_)(?!.*wav.*)"
        list_Play = []
        list_Play.append(re.findall(regex_playString, log)[-1])

        ts_playString = unique(
            list_Play)  # picks only response log lines. Ignores toneup and tonedown. Gives a playstring list

        print 'Session start: ', ts_PTT, 'Session end: ', ts_playString
        return latency(ts_PTT, ts_playString)


# function to calculate latency
def latency(ts_PTT, ts_playString):
    return ts_playString - ts_PTT + 600


# function to reverse a list of strings
def rever(strings):
    return [x[::-1] for x in strings]


# function to pick timestamp from log and convert it to integer
def stripper(playstring_list):
    response_timestamp = 0
    regexp = "[^\n]\d\d\d\d\d\d\d\d\d\d"
    for playstring in playstring_list:
        stripped_list = re.findall(regexp, playstring)  # picks only timestamps from the log line
        for tss in stripped_list:
            response_timestamp = int(tss.replace('_', ''))
    return response_timestamp


# function to get unique values
def unique(list1):
    # insert the list to the set
    list_set = set(list1)
    unique_list = (list(list_set))  # removes duplicate playstring values from list
    response_timestamp = stripper(unique_list)
    return response_timestamp


# function to generate csv file
def write_csv(latency):
    with open('output.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)

        header = ['Utterance', 'Latency(milliseconds)']

        writer.writerow(header)

        writer.writerow(('Play FM', latency))  # TODO: Enter correct command


# main function
if __name__ == '__main__':
    response_timestamp = reader('log')
    print 'Latency: ', response_timestamp
    write_csv(response_timestamp)
