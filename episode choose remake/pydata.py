import json

def pydata_load(data="data"):
    if data == "all":
        with open("episode choose remake/pydb.json", encoding="utf-8") as f:
            pydata = json.load(f)
            return pydata
    with open("episode choose remake/pydb.json", encoding="utf-8") as f:
        pydata = json.load(f)[data]

    return pydata

def pydata_save(data, database="data"):
    pydata = pydata_load("all")
    pydata[database] = data
    with open("episode choose remake/pydb.json", "w", encoding="utf-8") as f:
        json.dump(pydata, f)

if __name__ == "__main__":
    d = pydata_load()
    d["last_update"] = 123123

    pydata_save(d)