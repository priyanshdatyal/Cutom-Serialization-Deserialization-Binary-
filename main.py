
import ast


def encryptInt(num):
    return "{0:b}".format(num)

def decryptInt(binary):
    return int(binary, 2)
    
def encryptFloat(num):
    beforeDecimal = int(num)
    afterDecimal = int(str(num).split(".")[1])

    return beforeDecimal,afterDecimal

def decryptFloat():
    pass

def encryptString(data):
    return '00100000'.join(format(ord(i),'b') for i in data )

def decryptString(data):
    str_data=''
    for i in range(0, len(data), 7):
        temp_data = data[i:i + 7]
        
        decimal_data = decryptInt(temp_data)
        
        str_data = str_data + chr(decimal_data)

    return str_data

def getSymbol(obj):
    symbol="\'"
    if(type(obj)==int):
        symbol="~"
    elif (type(obj)==str):
        symbol="\'"
    elif (type(obj)==float):
        symbol="⌂"
    return symbol

def printDict(res,dictionary):
    count = 0
    for k, v in dictionary.items():
        if isinstance(v, dict):
            res = res + encryptString(str( "\n\'" + k + "\'" +":{"))
            res=printDict(res,v)
            count +=1
        else:
            symbol=''
            if isinstance(v,list):
                res=res+encryptString( str("\n\"" + k + "\"" +":["))
                for i in range(len(v)):
                    symbol=getSymbol(v[i])
                    res=res+encryptString(str(symbol+v[i]+symbol))
                    res=res+"0010000010110000100000"
                res+=encryptString("]")
                res=res+"0010000010110000100000"
            else:
                symbol=getSymbol(v)
                if(symbol=="\'"):
                    res=res+encryptString(str("\'"+k+"\'"+":" +symbol+v+symbol))
                elif(symbol=="~"):
                    res=res+encryptString(str("\'"+k+"\'"+":"))+"00100000111111000100000"+encryptInt(v)
                else:
                    beforeDecimal,afterDecimal=encryptFloat(v)
                    res=res+encryptString(str("\'"+k+"\'"+":"))+"00100000111111000100000"+encryptInt(beforeDecimal)+"0010000010111000100000111111000100000"+encryptInt(afterDecimal)
                res=res+"0010000010110000100000"

        while(count):
            res=res+encryptString(str("\n}"))
            res=res+"0010000010110000100000"
            count-=1
    return res
        

def writeToFile(data):
    f = open("dictionary.txt", "w")
    f.write(data)
    f.close()

def isFileFormatRight():
    text_file = open('dictionary.txt', "r")
    data = set(text_file.read())
    if(" " in data):
        print("Error!(Incorrect File Format) Your file contains space( \' \') character")
        return False
    if(data!={'0', '1'}):
        print("Error!(Non Binary File) Your dile contains non binary digits")
        return False
    return True

def deserialize():
    ans = ''
    insert=True
    if(isFileFormatRight()):
        with open('dictionary.txt','r') as datafile:
            for line in datafile:     
                for word in line.split("00100000"):        
                    if(insert):
                        ans=ans+str(decryptString(word))
                        pass
                    else:
                        ans=ans+str(decryptInt(str(word)))
                        insert=True
                    if(word=="1111110"):
                        insert=False
    else:
        exit()

                    

    return ans

def serialize(dictionary):
    res = encryptString(str("{"))
    res=printDict(res,dictionary)+encryptString(str("\n}"))
    writeToFile(res)



def main():
    dictionary = dict({'test':"!",'@cost':{'$abc': "#joke", 'df%': "^jokes"}, 
                        '&ghi':"*joker",'(liver':")monkey",'hitit':{'hell':"life@124",'Nice':"makeit"},'hitit1':{'hellOO':"life",'Nice':"makeit"},
                        'list1':['shit1',"shit2"],'hitit12':{'hellO':"life",'Nice':"makeit"},"number1":100,"number2":20,"float1":10.2345,"float2":20.22,
                        "1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"0":0})
    
    # Writing to a file in binary format
    serialize(dictionary)

    # Reading from the binary format file 
    resultDedString=deserialize()

    resultDedString = str(resultDedString).replace("\n","").replace(",}","}").replace(",]","]").replace("~","")
    
    print("------------------------------------------Result in String Format(DataType)------------------------------------\n")
    print(f" Resulted String after reading file :\n {resultDedString} \n")
    print(f" Final dictionary type  : {type(resultDedString)} ")
    

    resultDictionary = ast.literal_eval(resultDedString)

    print("--------------------------------------------After converting to dictionary------------------------------------\n")

    print(f" Resulted String to Dictionary  :\n {resultDedString} \n")
    print(f" Final dictionary type  : {type(resultDictionary)} ")
    exit()






if __name__ == "__main__":
    main()