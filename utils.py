import json

def load_json(path):
    with open(path, 'r') as f:
        content = json.loads(f.read())
    return content

def write_json(path, content, indent=4):
    with open(path, 'w') as f:
        f.write(json.dumps(content, indent=indent))

def clamp(value, min1, max1, min2, max2):
    return min2 + (max2-min2)*((value-min1)/(max1-min1))