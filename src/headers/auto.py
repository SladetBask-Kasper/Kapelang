import re

def getBetweem
pattern = str1+"(.*)"+str2
compiled = re.compile(pattern)

ms = compiled.search(fbhandle.read())
print ms.group(1).strip()
