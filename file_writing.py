import os

fp = open("hello.txt",'w')
num = 10
line = "%d"%num
fp.write(line)
fp.flush()
os.fsync(fp.fileno())

num = 11
line = "%d"%num
fp.write(line)
fp.flush()
os.fsync(fp.fileno())

n = 1/0

print n
