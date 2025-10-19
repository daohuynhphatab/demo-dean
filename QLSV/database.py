path='D:\code\doan\QLSV.txt'
def save(line):
    try:
        f=open(path,'a',encoding='utf8').write(line+'\n')
        f.writelines(line+'\n')
        f.close()
    except :
        pass
def read():
    sv=[]
    try:
        f=open(path,'r',encoding='utf8')
        for i in f:
            data = i.strip()
            arr = data.split('-')
            sv.append(arr)
        f.close()
    except:
        pass
    return sv
 