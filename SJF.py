# -*- coding: utf-8 -*-
"""
SJF
"""

import csv

def ready_sort(e):
  return e[1][0]
  

class process(object):
    
    p_time = 0      #program timer
    
    Ttr = []      #turnaround time for each process
    Tw = []       #waiting time for each process
    Tr = []       #Response time for each program
    
    num_process = 0  #find total num of processes to run
    io_time = 0      #find total time CPU is NOT running because CPU running time = TTr - io time
         
    p_bursts = []    #find total burst time of each process because tw[process] = TTr[process] - p_bursts[process] 
    last_num = False #if the last number of a process list is true do something
    
    #make each queue a list because python treats lists as objects
    p_ready = []    #list of processes in ready
    p_running = []  #list of process in running
    p_waiting = []  #list of prosesses in waiting


    """ 
    Name: process default initialize
    
    Description: 
        
    for every list in p list add to the ready queue
    find the total burst time of said program to find io time and cpu time for cpu utilization
    for every list add 1 to num of process to find total num of processes
    
    """
    def __init__(self, *lst): 
        print("Initializer: ")
        for x in range(0, len(lst)): #go through every lst element in p_lst
            self.num_process += 1    #add 1 for every process found
            self.p_ready.append([self.num_process, lst[x]]) #add num of process, the list to ready list
            
            total_burst = 0 #initialize total cpu/io burst of process to 0 for each process
           
            for y in lst[x]: #for every element in said list

                total_burst += y #add each io and cpu burst to toal burst
            
            self.p_bursts.append([self.num_process, total_burst]) #add num process, total burst of io/cpu to list of process bursts
            
            
        print(self.num_process, "Total Processes")  
        print("\nready: ", self.p_ready, "\nrunning: ", self.p_running, "\nwaiting: ", self.p_waiting)

    
    """ 
    Name: Ready queue to running queue
    
    Description: 
        
    if option is open and first element in wait is < program timer
    add first element - program time to io time
    reset program timer to next element in waiting (get out of waiting time)
    
    else, any other time
    if ready list is not empty
    running list = first element in ready list
    remove the first element in ready
        
    """
    def ready_torunning(self):
        print("\nready to running-------------------------------")
        
        print("Program Timer: ", process.p_time)

        #get process out of waiting
        if(len(self.p_waiting) != 0 and self.p_waiting[0][0] < process.p_time): #if waiting list not empty and first element in waiting < program time
            process.io_time += (self.p_waiting[0][0] - process.p_time) # add first element of waiting - program time to io time
            process.p_time = self.p_waiting[0][0] #reset program time to next element waiting in wait list to get it out
            print("Program Timer: ", process.p_time)
            print("\nready: ", self.p_ready, "\nrunning: ", self.p_running, "\nwaiting: ", self.p_waiting)
    
            process.waiting_toready(self) # jump to waiting to ready 
            
        elif (len(self.p_ready) == 0 and len(self.p_waiting) != 0 and self.p_waiting[0][0] > process.p_time): #elif ready list empty and if waiting list not empty and first element in waiting < program time
            process.io_time += (self.p_waiting[0][0] - process.p_time) # add first element of waiting - program time to io time
            process.p_time = self.p_waiting[0][0]  #reset program time to next element waiting in wait list to get it out
            print("Program Timer: ", process.p_time)
            print("\nready: ", self.p_ready, "\nrunning: ", self.p_running, "\nwaiting: ", self.p_waiting)
    
            process.waiting_toready(self) # jump to waiting to ready
        
        else: #any other time 
            if len(self.p_ready) != 0: # if ready list not empty
                self.p_running = self.p_ready.pop(0) # running list = first element in ready/remove first element in ready

        print("\nready: ", self.p_ready, "\nrunning: ", self.p_running, "\nwaiting: ", self.p_waiting)


    """ 
    Name: running queue to waiting queue
    
    Description: 
        
    if running list is not an empty list
    create a new list of the previous running list without the burst 
    reset running list to empty
    
    """
    def running_towaiting(self):
        print("\nrunning to waiting-------------------------------")
        if self.p_running != []: # if running list is not an empty list
            print("self.p_running != [] ", self.p_running)
            # create a new list of the previous running list without the burst 
            temp_lst = [self.p_running[1][0] + process.p_time, self.p_running[0], self.p_running[1][1::] ]
            
            print(temp_lst)
            
            self.p_waiting.append(temp_lst) #append the waiting list with the new list 
            
            self.p_running = [] #reset running list to empty
        
        print("Program Timer: ", process.p_time)

        print("\nready: ", self.p_ready, "\nrunning: ", self.p_running, "\nwaiting: ", self.p_waiting)
     
        
    """ 
    Name: waiting queue to ready queue
    
    Description: 
        
    reset the wait list to sorted temp wait list
    find all processes in waiting list that are ready to move to ready list 
    if (process wait time <= program timer)
    
    """        
    def waiting_toready(self):
        print("\nwaiting to ready-------------------------------")
        
        print("Program Timer: ", process.p_time)

        remove_lst = [] #initialize an empty list for index of element in waiting to remove
        
        temp = self.p_waiting # create a new list = waiting list
        
        temp.sort() # sort new list by shortest wait time
        
        self.p_waiting = temp #reset the wait list to sorted temp wait list
        
        for x in range(0, len(self.p_waiting)): # for every element in wait list
            
            if self.p_waiting[x][0] <= process.p_time: # if first element in said list <= program timer
                
                remove_lst.append(x) # add index to list so can remove it later
                print(self.p_waiting[x][0], "<=", process.p_time)
        
                print("\nready: ", self.p_ready, "\nrunning: ", self.p_running, "\nwaiting: ", self.p_waiting)

        print(remove_lst, "-----------------------------------------------------")
        for x in remove_lst: #for every element in remove list

            self.p_ready.append(self.p_waiting[0][1::]) # add the ready element to ready (make ready)
            self.p_waiting.remove(self.p_waiting[0]) # clear the said list from waiting

            print("\nready: ", self.p_ready, "\nrunning: ", self.p_running, "\nwaiting: ", self.p_waiting)


    """ 
    Name: Run process
    
    Description: 
        
    if run list not empty
        if run list only has one item
            set flag to true to know the process last burst ran
        add burst time to program timer
        remove the burst time from run list
    if flag == true
        add the process num, (finished time) to ttr list
        empty the run list
        reset the flag to false
    jump to running to waiting
    
    """ 
    def run(self): 
        
        print("\nprocess running\n-------")
        
        if (self.p_running != []): #if run list not empty list
            
            if (len(self.p_running[1]) == 1): #if running index [1] has only one item in list
        
                process.last_num = True #set a flag to know the last CPU burst of a process ran
            
            process.p_time += self.p_running[1][0] #add the burst time to program timer
          
            #print("Program Timer: ", process.p_time)
            
            self.p_running[1].pop(0) #make new list without the burst
            
        if (process.last_num == True): # if last number flag set

            process.Ttr.append((self.p_running[0], process.p_time)) #add process num, program timer(finished at)
            
            self.p_running = [] # empty run list
    
            print("Add to Ttr: ", process.Ttr)
            
            process.last_num = False #reset the flag to false for next process
            
        print("\nready: ", self.p_ready, "\nrunning: ", self.p_running, "\nwaiting: ", self.p_waiting)
  
        process.running_towaiting(self) # jump to running to waiting
            
    
    """ 
    Name: wait process (gate)
    
    Description: 
        
    if wait list is empty
        jump to wait to ready
    if wait list not empty and flag == false
        jump to wait to ready
    
    """ 
    def wait(self): #run the burst for the process in running queue
        
        if len(self.p_waiting) == 0: #if wait list empty
            process.waiting_toready(self) #jump to wait to ready
        else: #if wait list not empty
            if process.last_num == False: #if flag == false
                print("\nprocess waiting\n-------")

                print("Program Timer: ", process.p_time)
                
                process.waiting_toready(self) #jump to wait to ready
     
    """ 
    Name: terminate program
    
    Description: 
        
    if all "queues" empty
    calculate all values
    output results and confirm
    
    """    
    def terminate(self): #if all "queues" empty output results and confirm
        if len(self.p_ready) == 0 and len(self.p_running) == 0 and len(self.p_waiting) == 0:
            
            print("\nProgram Terminated -------------------------------")
            
            print("\nProgram Terminated at time: ", process.p_time)
            print("\nall lists empty")
            print("\nready: ", self.p_ready, "\nrunning: ", self.p_running, "\nwaiting: ", self.p_waiting, "\n")
            
            process.Ttr.sort() # sort the ttr list by program number
            process.Tr.sort()
            
            
            for x in range(0, len(process.Ttr)): #for every element in ttr list
                process.Tw.append((x + 1, process.Ttr[x][1] - process.p_bursts[x][1])) #add process num, Tw time
            
            print("\n***RESULTS***\n", "\nTw: ", process.Tw, "\nTtr: ", process.Ttr, "\nTr: ", process.Tr)
            
            avg_tw = 0 #find total wait time for all processes
            for x in process.Tw:
                #print(x[1])
                avg_tw += x[1]
                
            avg_ttr = 0 #find total of total time running for all processes
            for x in process.Ttr:
                #print(x[1])
                avg_ttr += x[1]
                
            avg_tr = 0 #find total response time for all processes
            for x in process.Tr:
                #print(x[1])
                avg_tr += x[1]
                
            print("\nOpening new output file: Results.csv")
    
            # field names 
            fields = ['Process Number:', 'Tw', 'Ttr', 'Tr'] 
            new_lst = []
            averages = ["Averages: ", round(avg_tw/self.num_process, 2), round(avg_ttr/self.num_process, 2), round(avg_tr/self.num_process, 2)]
            
            for x in range(0, self.num_process):
                #print("Process Num: ", process.Tw[x][0], "Tw time: ", process.Tw[x][1], "Ttr time: ", process.Ttr[x][1], "Tr time: ", process.Tr[x][1])
                new_lst.append([process.Tw[x][0], process.Tw[x][1], process.Ttr[x][1], process.Tr[x][1]])
                
            # name of csv file 
            filename = "Results.csv"
                
            # writing to csv file 
            with open(filename, 'w', newline='') as csvfile:
                
                # creating a csv writer object 
                csvwriter = csv.writer(csvfile) 
                    
                # writing the fields 
                csvwriter.writerow(fields) 
                
                #input Data
                csvwriter.writerows(new_lst)
                
                #input averages
                csvwriter.writerow(averages)
            
            #print the results of all calculations
            print("\nAverage Tw: ", round(avg_tw/self.num_process, 2), "\nAverage Ttr: ", round(avg_ttr/self.num_process, 2), "\nAverage Tr: ", round(avg_tr/self.num_process, 2))
            print("\nCPU utilization: ", round(((process.p_time - process.io_time)/process.p_time)*100,2),"%")
            
            return True
        else:
            print("lists not empty--------------------------------------")
            return False
    
    """ 
    Name: start program
    
    Description: 
        
    kickstart the program by adding first list in ready to running and add (num, program timer) to Tr list
    stay in while loop untill all lists empty
         if run list is empty
             run ready to running
             if len of process Tr < num total process
                 add the process (num, program timer) to Tr list
         run program
         wait gate
    
    """  
    def start(self):
        
        print("\nready: ", self.p_ready, "\nrunning: ", self.p_running, "\nwaiting: ", self.p_waiting, "\n")
           
        while process.terminate(self) == False: #while loop as long as all lists not empty
            
            if self.p_ready != []:
                
                self.p_ready.sort(reverse=False, key=ready_sort)

                print("\n", self.p_ready)
                
        
            if len(self.p_running) == 0: #if running list is empty
                    
                process.ready_torunning(self) #move first item in ready to running and clear from ready list
                
                p_inTr = False
                
                if len(process.Tr) < self.num_process: #after move process to run if len of process Tr < num total process
                    
                    if len(process.Tr) == []: #if Tr list is empty
                        process.Tr.append((self.p_running[0], process.p_time)) #add the process num, Tr to Tr list
    
                    else: #if tr not empty                     
                        for x in process.Tr: #go through the process numbers in the Tr list
                            if x[0] == self.p_running[0]: #if the process num is already in the list
                                p_inTr = True #set flag, process already in list = true

                    if p_inTr == False:
                        process.Tr.append((self.p_running[0], process.p_time)) #add the process num, Tr to Tr list
                            
                               
            process.run(self) #run program
            process.wait(self) # wait gate
                    
        
    def __str__(self): # easy string printing
        return str(self.p_ready) #convert to type string


def main():
    #initialize the class process with list of lists
    p_lst = process([5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 5], [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8], [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6], [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3], [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4], [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8], [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10], [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6])
    #p_lst = process([6, 10, 4], [9, 15, 6], [3, 5, 2])
    
    print("\nStart --------------------------------------")
    p_lst.start() #start the program untill the lists all empty
    print("\nEnd --------------------------------------")

if __name__ == "__main__":
    main() #run main
    
    
    
    
    