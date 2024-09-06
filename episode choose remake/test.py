original_names = ['Fallout: New Vegas', 'BioShock Remastered']
name = 'Fallout: New Vegas: Old World Blues'

def check_name(name):
    if original_names[0] in name or original_names[1] in name: return True
    else: return False
    

print(check_name(name))