def truncate_string(s):
    if int(s[0]) % 3 == 0:
        return truncate_string(s[1:])
    elif int(s[-1]) % 3 == 0:
        return truncate_string(s[:-1])
    elif (int(s[0]) + int(s[-1])) % 3 == 0:
        return truncate_string(s[1:-1])
    else:
        return s
