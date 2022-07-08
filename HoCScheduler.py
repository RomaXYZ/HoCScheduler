import pandas as pd
import HelperStructures
from heapq import heapify, heappush, heappop
import random
from enum import Enum

# If you want to add more steward jobs, append this constant list
STEWARDJOBS = ['Board Representative', 'Labor Steward', 'Kitchen Manager', 'Food Shop Manager', 'Treasurer', 'Membership',
                   'Garden Manager', 'Meeting Fascilitator', 'Office Contact']

# If you want to add more columns to the Scheduler Excelsheet, append this list and keep it in the correct order from left to right
EXCELCOLUMNS = ['Job Name', 'Number of Hours', 'Day',
        'Time Start', 'Time End', 'Slots', 'Priority', 'Assignment']

# If you want to add more columns to the responses Excelsheet, append this list and keep it in the correct order from left to right
RESPONSECOLUMNS = ['Timestamp', 'What is your name?',
        'Availability for Monday', 'Availability for Tuesday', 'Availability for Wednesday', 'Availability for Thursday',
                'Availability for Friday', 'Availability for Saturday',
                            'Availability for Sunday', 'Which jobs would you prefer?',
                                    'Which jobs can you not do?']

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def main():
    
    # Ask the labor steward questions
    print('Labor Steward Questions:')
    print('Please answer all answers numerically and press the enter key')
    # This stores the number of dinner cooks to be performed in a week
    dinner_cook_num = int(input('How many dinner cooks?\n'))

    days = [0, 1, 2, 3, 4, 5, 6]
    dinner_cook_days = []
    if(dinner_cook_num > 0):
        print('Would you like to randomly select which days dinner cooks are performed?')
        if(int(input('Random(0), Your discretion(1)' + '\n')) == 0):
            # Random was selected
            days_found = 0
            while(days_found < dinner_cook_num):
                x = random.choice(days)
                if(not(x in dinner_cook_days)):
                    dinner_cook_days.append(x)
                    days_found += 1
                    
            
        else:    
            # The steward would like to select in which days dinner cooks are done
            print('Monday(0), Tuesday(1), Wednesday(2), Thursday(3), Friday(4), Saturday(5), Sunday(6)')
            for x in range(dinner_cook_num):
                answer = int(input('Specify day #' + str(x + 1) + '\n'))
                if(not (answer in dinner_cook_days)):
                    dinner_cook_days.append(answer)
                else:
                    while(answer in dinner_cook_days):
                        print("Please don't input a day you previously put in, answer rejected")
                        answer = int(input('Specify day #' + str(x + 1) + '\n'))
                    dinner_cook_days.append(answer)
                    
    #Print out which days have been selected
    print("Dinner Cook days you've selected:")
    for x in range(len(dinner_cook_days)):
        print(DAYS[dinner_cook_days[x]])            
    
    # This stores the number of fast cooks to be performed in a week
    fast_cook_num = int(input('How many fast cooks?\n'))
    fast_cook_days = []
    if(fast_cook_num > 0):
        print('Would you like to randomly select which days fast cooks are performed?')
        if(int(input('Random(0), Your discretion(1)' + '\n')) == 0):
            # Random was selected
            days_found = 0
            while(days_found < fast_cook_num):
                x = random.choice(days)
                if(not(x in fast_cook_days)):
                    fast_cook_days.append(x)
                    days_found += 1
                    
            
        else:    
            # The steward would like to select in which days fast cooks are done
            print('Monday(0), Tuesday(1), Wednesday(2), Thursday(3), Friday(4), Saturday(5), Sunday(6)')
            for x in range(fast_cook_num):
                answer = int(input('Specify day #' + str(x + 1) + '\n'))
                if(not (answer in fast_cook_days)):
                    fast_cook_days.append(answer)
                else:
                    while(answer in fast_cook_days):
                        print("Please don't input a day you previously put in, answer rejected")
                        answer = int(input('Specify day #' + str(x + 1) + '\n'))
                    fast_cook_days.append(answer)
                
    # Print out which days have been selected
    print("Fast Cook days you've selected:")
    for x in range(len(fast_cook_days)):
        print(DAYS[fast_cook_days[x]])
        
    # This stores the number of garden helpers to be performed in a week
    garden_helper_num = int(input('How many garden helpers?\n'))
    
    
    # Allocate all jobs and put into the unfulfilled job array
    excelsheet = pd.read_excel(r'C:\Users\valde\Desktop\GitHub\HoCScheduler\House of Commons, Jobs.xlsx')
    df = pd.DataFrame(excelsheet, columns = EXCELCOLUMNS)
    
    # Array of unfulfilled jobs, initially full
    unfulfilled_jobs = []
    # Array of fulfilled jobs, initially empty
    fulfilled_jobs = []
    
    #Iterate through each job and allocate
    for ind in df.index:
        # Get the job name
        name = (df['Job Name'][ind])
        # Get the number of hours rewarded by this job
        hours = df['Number of Hours'][ind]
        # Get the day of the job
        day = df['Day'][ind]
        # Get the time start of availability
        time_start = df['Time Start'][ind]
        # Get the time end of availability
        time_end = df['Time End'][ind]
        # Get the number of people that can be allocated to this job
        slots = df['Slots'][ind]
        # Get the priority of this job
        priority = df['Priority'][ind]
        # Get the assignment, if it has one
        assignments = str(df['Assignment'][ind]).split(', ')

        # Take care of the Dinner Clean, Lunch Clean, Dinner Cook and Fast Cook edge cases here..
        if (name == 'Dinner Cook'):
            # You know that there are x days that dinner clean is to be performed, and know when it's going to happen
            for x in range(len(dinner_cook_days)):
                tempday = DAYS[dinner_cook_days[x]]
                # Allocate the job
                this_job = HelperStructures.Job(name, hours, tempday, time_start, time_end, slots, priority, assignments)
                unfulfilled_jobs.append(this_job)

        elif (name == 'Fast Cook'):
            for x in range(len(fast_cook_days)):
                tempday = DAYS[fast_cook_days[x]]
                # Allocate the job
                this_job = HelperStructures.Job(name, hours, tempday, time_start, time_end, slots, priority,
                                                assignments)
                unfulfilled_jobs.append(this_job)
        elif (name == 'Dinner Clean'):
            for x in range(7):
                tempday = DAYS[x]
                # Allocate the job
                this_job = HelperStructures.Job(name, hours, tempday, time_start, time_end, slots, priority,
                                                assignments)
                unfulfilled_jobs.append(this_job)

        elif (name == 'Lunch Clean'):
            for x in range(7):
                tempday = DAYS[x]
                # Allocate the job
                this_job = HelperStructures.Job(name, hours, tempday, time_start, time_end, slots, priority,
                                                assignments)
                unfulfilled_jobs.append(this_job)
        else:
            # Allocate the job
            this_job = HelperStructures.Job(name, hours, day, time_start, time_end, slots, priority, assignments)
        
            unfulfilled_jobs.append(this_job)
        
    
    #Read all the data from the responses excelsheet...
    excelsheet = pd.read_excel(r'C:\Users\valde\Desktop\GitHub\HoCScheduler\House of Commons, Scheduler (Responses).xlsx')
    df = pd.DataFrame(excelsheet, columns = RESPONSECOLUMNS)
    
    # Array of people being scheduled in this program...
    free_people = []
    taken_people = []
    
    #Iterate through each person and allocate...
    for ind in df.index:
        # Get the name
        name = (df['What is your name?'][ind])
        
        # Generate the schedule of each person
        rows, cols = (7, 14)
        day_availability = [[0]*cols]*rows
        
        day_availability[0] = df['Availability for Monday'][ind]
        day_availability[1] = df['Availability for Tuesday'][ind]
        day_availability[2] = df['Availability for Wednesday'][ind]
        day_availability[3] = df['Availability for Thursday'][ind]
        day_availability[4] = df['Availability for Friday'][ind]
        day_availability[5] = df['Availability for Saturday'][ind]
        day_availability[6] = df['Availability for Sunday'][ind]
        
        schedule = HelperStructures.Schedule(day_availability)
        
        # Generate the preferences of each person
        preferences = str(df['Which jobs would you prefer?'][ind]).split(', ')
        # Generate the restrictions of each person
        restrictions = str(df['Which jobs can you not do?'][ind]).split(', ')
        
        person = HelperStructures.Person(name, schedule, preferences, restrictions)
        free_people.append(person)
    
    
    # Go through each job and make sure that each hard-coded assignment is reflected...
    for x in range(len(unfulfilled_jobs)):
        if(not (unfulfilled_jobs[x].assignments[0] == 'nan')):
            # This assignment is not empty!
            # Update these people's hours!
            for j in range(len(unfulfilled_jobs[x].assignments)):
                name = unfulfilled_jobs[x].assignments[j]
                index = HelperStructures.findNameinPeople(name, free_people)
                if(index != -1):
                    free_people[index].hours += unfulfilled_jobs[x].hours
            # If the number of assignments is equal to the number of slots, fulfill..
            if(len(unfulfilled_jobs[x].assignments) == unfulfilled_jobs[x].slots):
                fulfilled_jobs.append(unfulfilled_jobs[x])
        # If this is a steward job without any assignment, fulfill..
        else:
            for y in range(len(STEWARDJOBS)):
                if(str(STEWARDJOBS[y]) == unfulfilled_jobs[x].name):
                    fulfilled_jobs.append(unfulfilled_jobs[x])
                
    # Deallocate any unfulfiled jobs which already have the numbers of slots equal to hard-coded candidates..
    for x in range(len(fulfilled_jobs)):
        unfulfilled_jobs.remove(fulfilled_jobs[x])
    
    # Check if any stewards are full of work now...
    for x in range(len(free_people)):
        if(free_people[x].hours >= 4):
            taken_people.append(free_people[x])
    for x in range (len(taken_people)):
        free_people.remove(taken_people[x])
    
    # The actual scheduling program starts below here...
    HelperStructures.printCurrentArrays(unfulfilled_jobs, fulfilled_jobs, free_people, taken_people)
    
    # Sort unfulfilled jobs by priority
    priorityHeap = []

    # Store into the priorityHeap the unfulfilled job's priority, name and index
    for x in range(len(unfulfilled_jobs)):
        heappush(priorityHeap, (unfulfilled_jobs[x].priority, unfulfilled_jobs[x].name, x))

    #Print the mappings of the priority heap
    # for x in range(len(priorityHeap)):
    #     print(priorityHeap[x])

    # Keep working until you've done a complete pass on the priorityHeap and that there are still free people to assign work
    while(priorityHeap != [] and free_people != []):
        # Pop a unfulfilled job
        working_job = unfulfilled_jobs[heappop(priorityHeap)[2]]

        # Create a list of available people... i,e who's schedule matches the needs of this job...
        available_people = []
        for x in range(len(free_people)):
            this_schedule = free_people[x].schedule
            # Is this person's schedule compatible with the job?

            start = str(working_job.time_start)
            end = str(working_job.time_end)
            if(not ("Flex" in str(working_job.time_start))):
                start = str(working_job.time_start).replace(":", "")[:-2]
                end = str(working_job.time_end).replace(":", "")[:-2]

            if("Flex" in start or "Flex" in end):
                # This person is available for this job
                available_people.append(free_people[x])

            else:
                # More work needs to be done to figure out if this person is available
                matching_schedule = 0
                if (not (this_schedule.Availability[DAYS.index(working_job.day)] == [])):
                    # This person has some availability on the day of this job
                    # The goal is to find a block of availability within the person's availability
                    time_index = int(HelperStructures.roundDownHour(str(working_job.time_start).replace(":", "")[:-2]))
                    hour_blocks = int(working_job.hours)
                    hours_worked = 0


                    while(time_index < int(HelperStructures.roundUpHour(str(working_job.time_end).replace(":", "")[:-2])) and matching_schedule == 0):
                        timeA = time_index + 100
                        hours_worked = 0

                        potential_match = 0
                        while(timeA <= int(HelperStructures.roundUpHour(str(working_job.time_end).replace(":", "")[:-2])) and hours_worked < hour_blocks and potential_match == 0):

                            if(HelperStructures.checkHorario(timeA) in this_schedule.Availability[DAYS.index(working_job.day)]):
                                # Person can work this hour
                                hours_worked += 1
                            else:
                                # This person needs to work this hour to be eligable, so they're not eligable
                                potential_match = 1

                            timeA += 100

                        if(hours_worked == hour_blocks):
                            # Match
                            matching_schedule = 1

                        # Try again
                        time_index += 100

                else:
                    # This person has no availability on this day, do not add to the list
                    pass

                if(matching_schedule == 1):
                    # We have a match!
                    available_people.append(free_people[x])

        for u in range(len(available_people)):
            print(working_job.name + " " + working_job.day + " " + available_people[u].name)

if __name__ == '__main__':
    main()