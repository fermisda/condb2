import getopt
import sys
from datetime import datetime

from condb2.ConDB import ConDB
from condb2.timelib import text2datetime

Usage = """
python read_data.py [options] <database name> <table_name> <column>,...
options:
    -h <host>
    -p <port>
    -U <user>
    -w <password>

    -n do not print values, print only number of rows retruned

    -t <time>   default = now
    -t <time0>...<time1>
    -T <tag>
    -d <data_type>       default = common
    -c <channel>-<channel>      channel range
"""

data_type = None
tag = None
dbcon = []
t0 = datetime.now()
t1 = t0
channel_range = None
print_values = True

opts, args = getopt.getopt(sys.argv[1:], 'h:U:w:p:t:d:T:c:n')

if len(args) < 3 or args[0] == 'help':
    print(Usage)
    sys.exit(0)

for opt, val in opts:
    if opt == '-h':
        dbcon.append("host=%s" % (val,))
    elif opt == '-p':
        dbcon.append("port=%s" % (int(val),))
    elif opt == '-U':
        dbcon.append("user=%s" % (val,))
    elif opt == '-w':
        dbcon.append("password=%s" % (val,))
    elif opt == '-t':
        words = val.split('...',1)
        t0 = text2datetime(words[0])
        t1 = t0
        if len(words) > 1:
            t1 = text2datetime(words[1])
    elif opt == '-T':
        tag = val
    elif opt == '-d':
        data_type = val
    elif opt == '-c':
        range = val.split('-')
        channel_range = (int(range[0]), int(range[1]))
    elif opt == '-n':
        print_values = False


dbcon.append("dbname=%s" % (args[0],))

dbcon = ' '.join(dbcon)
tname = args[1]
columns = args[2].split(',')
db = ConDB(dbcon)
table = db.table(tname, columns)

#data, iov = table.getData(t, data_type=data_type, tag=tag)
#channels = data.keys()
#channels.sort()
#for c in channels:
#    print c, iov[c], data[c]

if t1 == t0:
    data = table.getDataIter(t0, data_type=data_type, tag=tag,
        channel_range = channel_range)
else:
    data = table.getDataIntervalIter(t0, t1, data_type=data_type, tag=tag,
        channel_range = channel_range)

print("read_data: returned from table.getDataIntervalIter")
n = 0
for tup in data:
    c, tv = tup[:2]
    values = tup[2:]
    if print_values:
        print(c, tv, values)
    n += 1
print("returned %d rows" % (n,))
