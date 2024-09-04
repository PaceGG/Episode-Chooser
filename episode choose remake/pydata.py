import json

def pydata_load(data="data"):
    with open("episode choose remake/pydb.json", encoding="utf-8") as f:
        pydata = json.load(f)[data]

    return pydata

def pydata_save(data, database="data"):
    pydata = pydata_load()
    pydata[database] = data
    with open("episode choose remake/pydb.json", "w", encoding="utf-8") as f:
        json.dump(pydata, f)