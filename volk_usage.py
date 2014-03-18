#!/usr/bin/env python
import re,pprint,os
from subprocess import Popen, PIPE
from collections import Counter

p1 = Popen(["grep","-R","volk_", "gnuradio"], stdout=PIPE)
output = p1.communicate()[0];
sre = re.compile("(.*):.*(volk_[^\(]+).*");
useful_types = [".cc",".cc.t",".h"]
uses = [];
for vu in output.split("\n"):
    r = sre.search(vu);
    try:
        filename = r.group(1);
        kernel = r.group(2);

        # ignore volk subdir
        if(filename.startswith("gnuradio/volk")):
            continue;
    
        # only care about certain file types
        if(not reduce(lambda a,b: a or b, map(lambda x: filename.endswith(x), useful_types) )):
            continue;
 
        # show mappings
        #print "%s ---> %s"%(filename, kernel);
        uses.append( (filename,kernel) );
    except:
        #print "FAILURE: %s"%(vu)
        pass

# count usages
kcount = Counter( map(lambda x: x[1], uses) );
print "VOLK Kernel Usage Counts:"
pprint.pprint(dict(kcount));

# generate usage graph
f = open("digraph.dot","w");
f.write("digraph g {\noverlap = scalexy\n");
fl = []
kl = []
for (fn,k) in uses:
    if not fn in fl:
        fl.append(fn);
    if not k in kl:
        kl.append(k);
for fn in fl:
    f.write("\"%s\" [label = \"%s\"] [style = filled] [bgcolor = green]\n"%(os.path.split(fn)[1], fn));
for k in kl:
    f.write("\"%s\"\n"%(k));
for (fn,k) in uses:
    f.write("\"%s\" -> %s\n"%(os.path.split(fn)[1], k));
f.write("}\n");
f.close();
p2 = Popen(["neato","digraph.dot","-Tpng","-odigraph.png"], stdout=PIPE).wait()
p3 = Popen(["eog","digraph.png"]);
