import json

def pydata_load():
    with open("episode choose remake/pydb.json", encoding="utf-8") as f:
        pydata = json.load(f)

    return pydata

def pydata_save(pydata):
    with open("episode choose remake/pydb.json", "w", encoding="utf-8") as f:
        json.dump(pydata, f)