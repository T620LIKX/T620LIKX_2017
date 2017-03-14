import psycopg2


# Connect to the database
def connect_to_database(host, dbname, username, pw):
    conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)
    try:
        conn = psycopg2.connect(conn_string)
    except psycopg2.OperationalError as e:
        print('Connection failed!')
        print('Error message:', e)
        exit()
    cursor = conn.cursor()
    return cursor, conn


# Input: time as string (e.g. '9:30' or '10:45:28')
# Output: time as seconds (int)
def strtime2sec(t):
    tmp = t.split(':')
    if len(tmp) == 2:
        return int(tmp[0])*60*60 + int(tmp[1])*60
    elif len(tmp) == 3:
        return int(tmp[0])*60*60 + int(tmp[1])*60 + int(tmp[2])
    else:
        print('ERROR: Unknown time format: {}'.format(t))
        exit()


# Input: time as seconds (int or float)
# Output: time as string (e.g. '9:30', '10:45')
def sec2strtime(s):
    s = int(s+0.5)

    seconds = str(s % 60)
    if len(seconds) < 2:
        seconds = '0'+seconds

    s = s // 60

    minutes = str(s % 60)
    if len(minutes) < 2:
        minutes = '0'+minutes

    s = s // 60

    hours = str(s)

    if seconds == '00':
        return hours + ':' + minutes
    else:
        return hours + ':' + minutes + ':' + seconds

