import sys
try:
#    import org.apache.hadoop.io.Text as Text;
    import java.lang.System as System
    from com.xhaus.jyson import JysonCodec as json
except ImportError: #cpython
    Text = str
    import json

def map(key, value, context):
    try:
        payload = json.loads(value)
    except:
        e = sys.exc_info()[0]
        context.write(Text("exception:%s" % e), Text(key))
        return

    record = False
    try:
        ch = payload['chromeHangs']
        if type(ch) == dict:
            record = len(ch['memoryMap']) > 0
    except KeyError:
        pass

    try:
        lw = payload['lateWrites']
        if type(lw) == dict:
            record = record or len(lw['memoryMap']) > 0
    except KeyError:
        pass

    if record:
        outkey = Text(value)
        context.write(outkey, Text())
    
#def reduce(key, values, context):
#    context.write(key, Text())

class DummyContext:
    def __init__(self):
        pass
    def write(self, a, b):
        print (a,b)

if __name__ == "__main__":
    f = open(sys.argv[1])
    for l in f.readlines():
        map("", l, DummyContext)
