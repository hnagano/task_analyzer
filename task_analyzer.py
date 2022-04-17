# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import csv

task_dict = {
        "task_1" : 0,
        "task_2" : 1,
        #  "893d000" : 0,
        #  "893d000" : 1,
        #  "89c0000" : 2,
        #  "8a43000" : 3,
        #  "89c0000" : 4,
        #  "8a43000" : 5,
        #  "8ac6000" : 6,
        #  "8ac6000" : 7,
        }


class Event(object):
    def __init__(self):
        self.type = ''
        self.id = -1
        self.time = 0
        pass

    def __repr__(self):
        return "<Event type=%s id=%d time=%f>" % (self.type, self.id, self.time)

class RunInfo(object):
    def __init__(self, id, startTime, endTime):
        self.id = id
        self.startTime = startTime
        self.endTime = endTime

    def __repr__(self):
        return "<RunInfo id='%d' startTime='%f' endTime='%f'>" % (self.id, self.startTime, self.endTime)

class TaskGraph(object):
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.runinfo_list = []
        pass

    #def set_range(self, x_range):
        #self.x_range = x_range
        #pass

    def add_run_info(self, runinfo_list):
        self.runinfo_list = runinfo_list

    def show(self):
        y_max = 0
        x_min = 0xFFFFFFFF
        x_max = 0
        for elem in self.runinfo_list:
            x = elem.startTime
            y = elem.id * 1
            width = elem.endTime - elem.startTime
            height = 1
            rect = plt.Rectangle((x, y),width, height, fc="#000077")
            self.ax.add_patch(rect)
            if y + height > y_max:
                y_max = y + height
            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x
            
        self.x_range = (x_min, x_max)
        plt.xlim(self.x_range)
        plt.ylim((0, y_max))
        plt.gca().invert_yaxis()
        #  text = plt.Text(-50, 0.5, 'Task 1')
        #  plt.gca().add_artist(text)
        #  plt.text(-50, 0.5, 'Task 1')
        my_yticks = []
        y_ticks_num = []
        for item in task_dict.items():
            index = item[1]
            name = item[0]
            my_yticks.insert(index, name)
            y_ticks_num.insert(index, 0.5 + index * 1)
        print(my_yticks)
        print(y_ticks_num)
        plt.yticks(y_ticks_num, my_yticks)
        #  plt.tick_params(labelleft='off')
        plt.show()
        

class SectionInfo(object):
    def __init__(self, start_symbol, end_symbol):
        self.start_symbol = start_symbol
        self.end_symbol = end_symbol

def generate_run_sequence(eventlist):
    runinfo_list = []
    section = SectionInfo('TS_Start', 'TS_End')
    startTime_record = {}
    
    #parse event list into run info
    for event in eventlist:
        if event.type == section.start_symbol:
            startTime = event.time
            startTime_record[event.id] = startTime
            print(type(event.id))
        elif event.type == section.end_symbol:
            endTime = event.time
            startTime = startTime_record[event.id]
            #  print("append {},{},{} ".format(event.id, str(startTime), str(endTime)))
            runinfo_list.append(RunInfo(event.id, startTime, endTime))
            del startTime_record[event.id]


    return runinfo_list

def read_eventlist_csv(filename):

    eventlist = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        # parse csv into event
        for row in reader:
            event = Event()
            task_name = row[0]
            event.id = task_dict[task_name]
            event.type = row[1]
            event.time = float(row[2])
            eventlist.append(event)
    return eventlist

def main():
    graph = TaskGraph()

    eventlist = read_eventlist_csv('sample_log.csv')
    #  eventlist = read_eventlist_csv('./posix/log_sample_posix.csv')
    print(eventlist)

    runinfo_list = generate_run_sequence(eventlist)
    print(runinfo_list)

    graph.add_run_info(runinfo_list)
    #graph.set_range((22648, 26607))
    graph.show()

if __name__ == '__main__':
    main()

