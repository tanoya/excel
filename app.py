# coding:utf-8

import re
import json

class LocalFile:
    """主要用于文件的读写"""
    
    dir = "./screen/"
    file_name = "tmp.txt"
    filt_out_name = "out.txt"
    body = []
    
    B = 1
    KB = 1024 * B
    MB = 1024 * KB
    GB = 1024 * MB
    TB = 1024 * GB
    
    def __init__(self, dir, file_name):
        if dir:
            self.dir = dir
        if file_name:
            self.file_name = file_name

    def handle(self):
        path = self.dir + self.file_name
        with open(path, "r", encoding='utf-8') as f:
            data = f.readline()
            while data:
                item = self.handleLine(data)
                if item:
                    self.body.append(item)
                data = f.readline()

    def handleLine(self, line):
        if not line:
            return None
        arr = line.split('\t')
        if len(arr) < 8:
            return None
        if not arr[0] or not arr[4] or not arr[7]:
            return None
        pat = r"(\d+)([G|g|m|M])"
        matGroup = re.match(pat, arr[4])
        if matGroup:
            cap = matGroup.group(1)
            unit = matGroup.group(2)
            if "g" == unit.lower():
                cap = int(cap) * self.GB
            elif "m" == unit.lower():
                cap = int(cap) * self.MB
            return {"app":arr[0], "capacity":cap, "admin":arr[7]}
        else:
            return {"app":arr[0], "capacity":5 * self.TB, "admin":arr[7]}
    
    def write(self):
        path = self.dir + self.filt_out_name
        with open(path, "w", encoding='utf-8') as f:
            ret = json.dumps(self.body)
            f.write(ret)

if __name__ == "__main__":
    lf = LocalFile(None, None)
    lf.handle()
    lf.write()
    print(lf.body)
