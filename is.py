import sys

#check types
def checkstring(string):
    if string.startswith('"'):
        if string.endswith('"'):
            return True
        else:
            return False
    elif string.startswith("'"):
        if string.endswith("'"):
            return True
        else:
            return False

def checkint(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def checkfloat(floatnum):
    try:
        float(floatnum)
        return True
    except ValueError:
        return False

def checkvar(varn, vars):
    try:
        if vars[varn] == "hello":
            pass
        return True
    except KeyError:
        return False

def checklist(slist):
    if slist.startswith("["):
        if slist.endswith("]"):
            return True
        else:
            return False
    else:
        return False

def checkdic(dic):
    if dic.startswith("{") and dic.endswith("}"):
        return True
    else:
        return False



#calculate
def calculate(tree, vars):
    #check operator
    if tree[2] == "+":
        return checktypes(vars, tree[1]) + checktypes(vars, tree[3])
    elif tree[2] == "-":
        return checktypes(vars, tree[1]) - checktypes(vars, tree[3])
    elif tree[2] == "*":
        return checktypes(vars, tree[1]) * checktypes(vars, tree[3])
    elif tree[2] == "/":
        return checktypes(vars, tree[1]) / checktypes(vars, tree[3])

#open files
def openfile(tree, vars):
    typeopen = ""
    if tree[2] == "write":
        typeopen = "w"
    elif tree[2] == "read":
        typeopen = "r"
    elif tree[2] == "writebytes":
        typeopen = "wb"
    elif tree[2] == "readbytes":
        typeopen = "rb"
    try:
        thefile = open(checktypes(vars, tree[1]), typeopen)
        vars[tree[3]] = thefile
    except Exception as e:
        print(e)
        sys.exit()
    return

#change
def changeToList(lists, vars):
    lists = lists[1:][:-1]
    lists = lists.split(",")
    newlist = []
    for i in lists:
        nospace = i.strip()
        if checkstring(nospace):
            newlist.append(nospace[1:][:-1])
        elif checkint(nospace):
            newlist.append(int(nospace))
        elif checkfloat(nospace):
            newlist.append(float(nospace))
        elif checkvar(nospace, vars):
            newlist.append(vars[nospace])
        elif checklist(nospace):
            newlist.append(changeToList(nospace, vars))
        else:
            print("Unknown value type: {}".format(nospace))
            sys.exit()
    return newlist

#check types
def checktypes(vars, thing):
    if checkstring(thing):
        return thing[1:][:-1]
    elif checkint(thing):
        return int(thing)
    elif checkfloat(thing):
        return float(thing)
    elif checkvar(thing, vars):
        return vars[thing]
    elif checklist(thing):
        return changeToList(thing, vars)
    elif checkdic(thing):
        try:
            return eval(thing)
        except:
            print("Invalid dictionary: {}".format(thing))
            sys.exit()
    else:
        print("ValueError: Unknown value type: {}".format(thing))
        sys.exit

def execi(cmd, vars):
        if cmd[0] == "print":
            print(checktypes(vars, cmd[1]))

        elif cmd[0] == "var":
            vars[cmd[1]] = checktypes(vars, cmd[3])
        
        elif cmd[0] == "calc":
            #set variable to result
            vars[cmd[4]] = calculate(cmd, vars)
        
        elif cmd[0] == "openf":
            openfile(cmd, vars)
        
        elif cmd[0] == "read":
            vars[cmd[2]] = vars[cmd[1]].read()

        elif cmd[0] == "write":
            vars[cmd[1]].write(checktypes(vars, cmd[2]))

        elif cmd[0] == "closef":
            vars[cmd[1]].close()

        elif cmd[0] == "stop":
            sys.exit()

#language
def execute():
    ast = parse()

    vars = {}

    for cmd in ast:
        execi(cmd, vars)

def tokenize():
    with open(sys.argv[1]) as f:
        content = f.read()
        contentsplit = content.split('\n')

        tokens = []
        for line in contentsplit:
            if line == '':
                continue
            elif line.startswith('#'):
                #continue if it's comment
                continue
            else:
                tokens.append(line.split(" "))
        return tokens

def parse(tokens=None):
    ast = []
    if tokens == None:
        tokens = tokenize()

    for token in tokens:
        if token[0] == "print":
            restofwords = ""
            for i in range(1, len(token)):
                restofwords += token[i] + " "
            restofwords = restofwords[:-1]
            ast.append(["print", restofwords])
        elif token[0] == "var":
            restofwords = ""
            for i in range(3, len(token)):
                restofwords += token[i] + " "
            restofwords = restofwords[:-1]
            ast.append(["var", token[1], token[2], restofwords])
        elif token[0] == "calc":
            ast.append(token)
        elif token[0] == "openf":
            ast.append(["openf", token[1], token[2], token[3]]) #token[1] is file name token[2] is open type read write readbytes writebytes. token[3] variable name.
        elif token[0] == "read":
            ast.append(["read", token[1], token[2]]) #token[1] is file var token[2] read result var
        elif token[0] == "write":
            towrite = ""
            for i in range(2, len(token)):
                if i != 2:
                    towrite = towrite + " " + token[i]
                else:
                    towrite += token[i]
            ast.append(["write", token[1], towrite]) #token[1] is file var token[2] thing to write
        elif token[0] == "closef":
            ast.append(["closef", token[1]]) #token[1] is file var
        elif token[0] == "stop":
            ast.append(["stop"])
        else:
            print("Unknown command: " + token[0])
            sys.exit()
    

    return ast

execute()