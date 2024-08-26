import ipdb

my_time = "4:33,6,3:6"

def time_sum(my_time):
    my_time = my_time.split(",")
    for i, time in enumerate(my_time):
        ipdb.set_trace()
        time = time.split(":")
        if len(time) == 2:
            time = int(time[0]) * 60 + int(time[1])
        else:
            time = int(time[0])
        my_time[i] = time
    my_time = sum(my_time)

my_time = time_sum(my_time)

print(my_time)