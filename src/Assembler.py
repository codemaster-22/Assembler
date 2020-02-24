
import sys

def jumpfunc(jump):
    if 'JGT'==jump:
        return '001'
    elif 'JEQ'==jump:
        return '010'
    elif 'JGE'==jump:
        return '011'
    elif 'JLT'==jump:
        return '100'
    elif 'JNE'==jump:
        return '101'
    elif 'JLE'==jump:
        return '110'
    else:
        return '111'
def computefunc(compute):
    if compute=='0':
        return '101010'
    elif compute=='1':
        return '111111'
    elif compute=='-1':
        return '111010'
    elif compute=='D':
        return '001100'
    elif compute=='-D':
        return '001111'
    elif compute=='D+1':
        return '011111'
    elif compute=='D-1':
        return '001110'
    elif compute=='!D':
        return '001101'
    elif '!' in compute:
        return '110001'
    elif '+1' in compute:
        return '110111'
    elif '-1' in compute:
        return '110010'
    elif 'D+' in compute:
        return '000010'
    elif 'D-' in compute:
        return '010011'
    elif '-D' in compute:
        return '000111'
    elif 'D&' in compute:
        return '000000'
    elif 'D|' in compute:
        return '010101'
    elif '-' in compute:
        return '110011'
    else:
        return '110000'

def main():
    count =int(sys.argv[1])
    files=[]
    for i in range(count):
        files.append(sys.argv[2+i])
    for file in files:
        with open(file) as myfile:
            contents=myfile.readlines()
            file=file[:-3]
            for i in range(len(contents)):
                s="//"
                if s in contents[i]:
                    j=contents[i].find(s)
                    contents[i]=contents[i][:j]
                contents[i]=''.join([x for x in contents[i].split(' ')])
                if '\n' in contents[i]:
                    j=contents[i].find('\n')
                    contents[i]=contents[i][:j]
            while '' in contents:
                contents.remove('')
            symbol={}
            j=0
            for i in contents:
                if i[0]=='(':
                    s=i[1:-1]
                    if s not in symbol.keys():
                        symbol[s]=j
                else:
                    j+=1
            for i in contents:
                if i[0]=='(':
                    contents.remove(i)
            for k in range(16):
                symbol['R'+str(k)]=k
            symbol['SP']=0
            symbol['LCL']=1
            symbol['ARG']=2
            symbol['THIS']=3
            symbol['THAT']=4
            symbol['SCREEN']=(2**14)
            symbol['KBD']=(2**15)-1
            j=16
            for i in range(len(contents)):
                if contents[i][0]=='@':
                    s=contents[i][1:]
                    if not(s.isnumeric()):
                        if s in symbol.keys():
                            s=str(symbol[s])
                        else :
                            symbol[s]=j
                            s=str(j)
                            j+=1
                    contents[i]="@"+s



            for i in range(len(contents)):
                if contents[i][0]=='@':
                    contents[i]=int(contents[i][1:])
                    contents[i]=bin(contents[i]).replace("0b","")
                    j=len(contents[i])
                    if(j<16):
                        contents[i]=('0'*(16-j))+contents[i]+'\n'
                else :
                    p=[x for x in ('0'*16)]
                    if '=' in contents[i]:
                        j=contents[i].find('=')
                        destination=contents[i][:j]
                        if 'M' in destination:
                            p[12]='1'
                        if 'D' in destination:
                            p[11]='1'
                        if 'A' in destination:
                            p[10]='1'
                        compute=(contents[i][j+1:])
                    elif ';' in contents[i]:
                        j=contents[i].find(';')
                        compute=contents[i][:j]
                        jump=contents[i][j+1:]
                        jump=jumpfunc(jump)
                        p[15]=jump[2]
                        p[14]=jump[1]
                        p[13]=jump[0]
                    if 'M' in compute:
                        p[3]='1'
                    compute=computefunc(compute)
                    for k in range(6):
                        p[4+k]=compute[k]
                    p[0]='1'
                    p[1]='1'
                    p[2]='1'
                    p=''.join(p)
                    p+='\n'
                    contents[i]=p
            with open(file+'.asm',mode='w') as myfile:
                myfile.write(''.join(contents))
if __name__ == "__main__":
    main()
     
