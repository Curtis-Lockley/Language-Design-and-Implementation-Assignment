def isFloat(num):
    try:
        float(num)
        return True
    except:
        return False

def toBool(string):
    if string.lower() == "true":
        return True
    return False
