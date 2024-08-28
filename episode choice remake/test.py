shift_range = {}


shift_range["test"] = 3

try: 
    shift_range["test2"] += 3
except:
    shift_range["test2"] = 3

try: 
    shift_range["test2"] += 3
except:
    shift_range["test2"] = 3

print(shift_range)