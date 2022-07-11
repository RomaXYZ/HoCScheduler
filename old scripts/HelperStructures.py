
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
        
        
def findNameinPeople(name, people):
    for x in range(len(people)):
        if (people[x].name == name):
            return(x)
    return(-1)
            
def printCurrentArrays(unfulfilled, fulfilled, free_people, taken_people):
    print("Printing unfulfilled array")
    for x in range(len(unfulfilled)):
        print(str(unfulfilled[x].name) + ", " + str(unfulfilled[x].day))
    print("...")
    print("...")
    print("...")
    print("Printing fulfilled array")
    for x in range(len(fulfilled)):
        print(str(fulfilled[x].name) + ", " + str(fulfilled[x].day))
    print("...")
    print("...")
    print("...")
    print("Printing free_people array")
    for x in range(len(free_people)):
        print(str(free_people[x].name) + " " + str(free_people[x].hours))
    print("...")
    print("...")
    print("...")
    print("Printing taken_people array")
    for x in range(len(taken_people)):
        print(str(taken_people[x].name) + " " + str(taken_people[x].hours))
        
    print("Printing done")

def roundUpHour(time):
    temptime = time[:2] + "00"

    integerleft = int(time[:-2])

    if(int(time[2:]) > 0):
        integerleft += 1

    if(integerleft > 23):
        integerleft = 0

    temptime = str(integerleft) + temptime[2:]

    return(temptime)

def roundDownHour(time):
    temptime = time[:2] + "00"

    integerleft = int(time[:-2])

    temptime = str(integerleft) + temptime[2:]

    return(temptime)


def checkHorario(hour):
    hour_string = str(hour)
    temp_string = hour_string[:len(hour_string) - 2]

    current_time = int(temp_string) - 9
    # Map to a time slot
    return(TIMESLOTS[current_time])
