with open('app.log', 'r') as log_file:
    lines = log_file.read().splitlines()
    time = lines[-1].split(';')[0]
    print(time)