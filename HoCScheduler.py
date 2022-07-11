import pandas as pd
from heapq import heapify, heappush, heappop
import random
from enum import Enum

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

# My structure and functions made for this project...

TIMESLOTS = ["8 AM - 9 AM", "9 AM - 10 AM", "10 AM - 11 AM", "11 AM - 12 PM", "12 PM - 1 PM",
             "1 PM - 2 PM", "2 PM - 3 PM", "3 PM - 4 PM", "4 PM - 5 PM", "5 PM - 6 PM", "6 PM - 7 PM",
             "7 PM - 8 PM", "8 PM - 9 PM", "9 PM - 10 PM", "10 PM - 11 PM", "11 PM - 12 PM"]


# Everyone should be allocated 4 hours
# This class dictates a person's attributes
class Person:
    def __init__(self, name, schedule, preferences, restrictions):
        self.name = name
        self.schedule = schedule
        self.preferences = preferences
        self.restrictions = restrictions
        self.hours = 0


# This class dictates a person's schedule
# Monday(0), Tuesday(1), Wednesday(2), Thursday(3), Friday(4), Saturday(5), Sunday(6)
class Schedule:
    def __init__(self, day_availability):
        self.Availability = []
        self.Availability.append(day_availability[0])
        self.Availability.append(day_availability[1])
        self.Availability.append(day_availability[2])
        self.Availability.append(day_availability[3])
        self.Availability.append(day_availability[4])
        self.Availability.append(day_availability[5])
        self.Availability.append(day_availability[6])

        # This class dictates the characteristics of a job to be assigned


# To the person
class Job:
    def __init__(self, name, hours, day, time_start,
                 time_end, slots, priority, assignments):
        self.name = name
        self.hours = hours
        self.day = day
        self.time_start = time_start
        self.time_end = time_end
        self.slots = slots
        self.priority = priority
        self.assignments = assignments

# ** Special array of persons and jobs

class Matching:
    def __init__(self):
        self.all_people = []
        self.all_jobs = []
        self.dictionary = []

        self.free_people = 0
        self.free_jobs = 0

    def add_people(self, person):
        self.all_people.append(person)
        self.free_people += 1

    def add_job(self, job):
        self.all_jobs.append(job)
        heappush(self.dictionary, (job.priority, len(self.all_jobs) - 1))
        self.free_jobs += 1

    def pop_job(self):
        return(heappop(self.dictionary))

    def forceAssignments(self):
        for x in range(len(self.all_jobs)):
            this_job = self.all_jobs[x]
            for y in range(len(this_job.assignments)):
                this_assignment = this_job.assignments[y]
                for z in range(len(self.all_people)):
                    if(this_assignment == self.all_people[z].name):
                        self.all_people[z].hours += this_job.hours


    def printArrays(self):
        print("Printing all people")
        for x in range(len(self.all_people)):
            print(str(self.all_people[x].name) + " h:" + str(self.all_people[x].hours))
        print("...")
        print("...")
        print("...")
        print("Printing all jobs")
        for x in range(len(self.all_jobs)):
            print(str(self.all_jobs[x].name + " a:" + str(" ".join(self.all_jobs[x].assignments))))
        print("...")
        print("...")
        print("...")
        print("Printing job dictionary")
        for x in range(len(self.dictionary)):
            print(str(self.dictionary[x][0]) + " in:" + str(self.dictionary[x][1]))


    ## ** Time Functions **
def roundUpHour(time):
    temptime = time[:2] + "00"

    integerleft = int(time[:-2])

    if (int(time[2:]) > 0):
        integerleft += 1

    if (integerleft > 23):
        integerleft = 0

    temptime = str(integerleft) + temptime[2:]

    return (temptime)


def roundDownHour(time):
    temptime = time[:2] + "00"

    integerleft = int(time[:-2])

    temptime = str(integerleft) + temptime[2:]

    return (temptime)


def checkHorario(hour):
    hour_string = str(hour)
    temp_string = hour_string[:len(hour_string) - 2]

    current_time = int(temp_string) - 9
    # Map to a time slot
    return (TIMESLOTS[current_time])



def main():

    # Ask the labor steward questions
    print('Labor Steward Questions:')
    print('Please answer all answers numerically and press the enter key')
    # This stores the number of dinner cooks to be performed in a week
    dinner_cook_num = int(input('How many dinner cooks?\n'))

    days = [0, 1, 2, 3, 4, 5, 6]
    dinner_cook_days = []
    if (dinner_cook_num > 0):
        print('Would you like to randomly select which days dinner cooks are performed?')
        if (int(input('Random(0), Your discretion(1)' + '\n')) == 0):
            # Random was selected
            days_found = 0
            while (days_found < dinner_cook_num):
                x = random.choice(days)
                if (not (x in dinner_cook_days)):
                    dinner_cook_days.append(x)
                    days_found += 1


        else:
            # The steward would like to select in which days dinner cooks are done
            print('Monday(0), Tuesday(1), Wednesday(2), Thursday(3), Friday(4), Saturday(5), Sunday(6)')
            for x in range(dinner_cook_num):
                answer = int(input('Specify day #' + str(x + 1) + '\n'))
                if (not (answer in dinner_cook_days)):
                    dinner_cook_days.append(answer)
                else:
                    while (answer in dinner_cook_days):
                        print("Please don't input a day you previously put in, answer rejected")
                        answer = int(input('Specify day #' + str(x + 1) + '\n'))
                    dinner_cook_days.append(answer)

    # Print out which days have been selected
    print("Dinner Cook days you've selected:")
    for x in range(len(dinner_cook_days)):
        print(DAYS[dinner_cook_days[x]])

        # This stores the number of fast cooks to be performed in a week
    fast_cook_num = int(input('How many fast cooks?\n'))
    fast_cook_days = []
    if (fast_cook_num > 0):
        print('Would you like to randomly select which days fast cooks are performed?')
        if (int(input('Random(0), Your discretion(1)' + '\n')) == 0):
            # Random was selected
            days_found = 0
            while (days_found < fast_cook_num):
                x = random.choice(days)
                if (not (x in fast_cook_days)):
                    fast_cook_days.append(x)
                    days_found += 1


        else:
            # The steward would like to select in which days fast cooks are done
            print('Monday(0), Tuesday(1), Wednesday(2), Thursday(3), Friday(4), Saturday(5), Sunday(6)')
            for x in range(fast_cook_num):
                answer = int(input('Specify day #' + str(x + 1) + '\n'))
                if (not (answer in fast_cook_days)):
                    fast_cook_days.append(answer)
                else:
                    while (answer in fast_cook_days):
                        print("Please don't input a day you previously put in, answer rejected")
                        answer = int(input('Specify day #' + str(x + 1) + '\n'))
                    fast_cook_days.append(answer)

    # Print out which days have been selected
    print("Fast Cook days you've selected:")
    for x in range(len(fast_cook_days)):
        print(DAYS[fast_cook_days[x]])

    # This stores the number of garden helpers to be performed in a week
    garden_helper_num = int(input('How many garden helpers?\n'))

    # Create a master jobs array
    excelsheet = pd.read_excel(r'C:\Users\valde\Desktop\GitHub\HoCScheduler\House of Commons, Jobs.xlsx')
    df = pd.DataFrame(excelsheet, columns=EXCELCOLUMNS)

    matching = Matching()


    # Allocate all the jobs available
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
                this_job = Job(name, hours, tempday, time_start, time_end, slots, priority,
                                                assignments)
                matching.add_job(this_job)

        elif (name == 'Fast Cook'):
            for x in range(len(fast_cook_days)):
                tempday = DAYS[fast_cook_days[x]]
                # Allocate the job
                this_job = Job(name, hours, tempday, time_start, time_end, slots, priority,
                                                assignments)
                matching.add_job(this_job)
        elif (name == 'Dinner Clean'):
            for x in range(7):
                tempday = DAYS[x]
                # Allocate the job
                this_job = Job(name, hours, tempday, time_start, time_end, slots, priority,
                                                assignments)
                matching.add_job(this_job)

        elif (name == 'Lunch Clean'):
            for x in range(7):
                tempday = DAYS[x]
                # Allocate the job
                this_job = Job(name, hours, tempday, time_start, time_end, slots, priority,
                                                assignments)
                matching.add_job(this_job)
        else:
            # Allocate the job
            this_job = Job(name, hours, day, time_start, time_end, slots, priority, assignments)

            matching.add_job(this_job)

    # Read all the data from the responses excelsheet...
    excelsheet = pd.read_excel(
        r'C:\Users\valde\Desktop\GitHub\HoCScheduler\House of Commons, Scheduler (Responses).xlsx')
    df = pd.DataFrame(excelsheet, columns=RESPONSECOLUMNS)

    # Iterate through each person and allocate...
    for ind in df.index:
        # Get the name
        name = (df['What is your name?'][ind])

        # Generate the schedule of each person
        rows, cols = (7, 14)
        day_availability = [[0] * cols] * rows

        day_availability[0] = df['Availability for Monday'][ind]
        day_availability[1] = df['Availability for Tuesday'][ind]
        day_availability[2] = df['Availability for Wednesday'][ind]
        day_availability[3] = df['Availability for Thursday'][ind]
        day_availability[4] = df['Availability for Friday'][ind]
        day_availability[5] = df['Availability for Saturday'][ind]
        day_availability[6] = df['Availability for Sunday'][ind]

        schedule = Schedule(day_availability)

        # Generate the preferences of each person
        preferences = str(df['Which jobs would you prefer?'][ind]).split(', ')
        # Generate the restrictions of each person
        restrictions = str(df['Which jobs can you not do?'][ind]).split(', ')

        person = Person(name, schedule, preferences, restrictions)
        matching.add_people(person)

    # Go through each job and make sure that each hard-coded assignment is reflected...
    matching.forceAssignments()

    # Take out the executive positions to remove a bug...
    for x in reversed(range(len(matching.all_jobs))):
        if(str(matching.all_jobs[x].day) == "Executive"):
            del matching.all_jobs[x]
            for y in reversed(range(len(matching.dictionary))):
                if(matching.dictionary[y][1] == x):
                    del matching.dictionary[y]


    while(matching.dictionary != [] and matching.free_people > 0):
        # Pop a unfulfilled job
        job_index = matching.pop_job()[1]
        working_job = matching.all_jobs[job_index]

        # Create a list of available people
        available_people = []
        for x in range(len(matching.all_people)):
            this_person = matching.all_people[x]
            if(this_person.hours < 4):
                # This person has the hours to take in work
                # Is this person's schedule compatible with this job?
                this_schedule = this_person.schedule
                start = str(working_job.time_start)
                end = str(working_job.time_end)
                if (not ("Flex" in str(working_job.time_start))):
                    start = str(working_job.time_start).replace(":", "")[:-2]
                    end = str(working_job.time_end).replace(":", "")[:-2]

                if ("Flex" in start or "Flex" in end):
                    # This person is available for this job
                    available_people.append(this_person)

                else:
                    # More work needs to be done to figure out if this person is available
                    matching_schedule = 0
                    if (not (this_schedule.Availability[DAYS.index(working_job.day)] == [])):
                        # This person has some availability on the day of this job
                        # The goal is to find a block of availability within the person's availability
                        time_index = int(
                            roundDownHour(str(working_job.time_start).replace(":", "")[:-2]))
                        hour_blocks = int(working_job.hours)
                        hours_worked = 0

                        while (time_index < int(roundUpHour(
                                str(working_job.time_end).replace(":", "")[:-2])) and matching_schedule == 0):
                            timeA = time_index + 100
                            hours_worked = 0

                            potential_match = 0
                            while (timeA <= int(roundUpHour(str(working_job.time_end).replace(":", "")[
                                                                             :-2])) and hours_worked < hour_blocks and potential_match == 0):

                                if (checkHorario(timeA) in this_schedule.Availability[
                                    DAYS.index(working_job.day)]):
                                    # Person can work this hour
                                    hours_worked += 1
                                else:
                                    # This person needs to work this hour to be eligable, so they're not eligable
                                    potential_match = 1

                                timeA += 100

                            if (hours_worked == hour_blocks):
                                # Match
                                matching_schedule = 1

                            # Try again
                            time_index += 100

                    else:
                        # This person has no availability on this day, do not add to the list
                        pass

                    if (matching_schedule == 1):
                        # We have a match!
                        available_people.append(this_person)


            else:
                # Find another person
                pass

        for y in range(len(available_people)):
            print(str(working_job.name) + " " + str(available_people[y].name))

        # You have an array of all the available people to match to this job...

if __name__ == '__main__':
    main()

