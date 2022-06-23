from sys import *
import ast

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
    print(tree)
    #check operator
    if tree[2] == "+":
        return checktypes(vars, tree[1]) + checktypes(vars, tree[3])
    elif tree[2] == "-":
        return checktypes(vars, tree[1]) - checktypes(vars, tree[3])
    elif tree[2] == "*":
        return checktypes(vars, tree[1]) * checktypes(vars, tree[3])
    elif tree[2] == "/":
        return checktypes(vars, tree[1]) / checktypes(vars, tree[3])

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
            raise ValueError("Unknown value type: {}".format(nospace))
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
            return ast.literal_eval(thing)
        except:
            raise Exception("Invalid dictionary: {}".format(thing))
    else:
        raise Exception("ValueError: Unknown value type: {}".format(thing))

#language
def execute():
    ast = parse()

    vars = {}

    for cmd in ast:
        if cmd[0] == "print":
            print(checktypes(vars, cmd[1]))

        elif cmd[0] == "var":
            vars[cmd[1]] = checktypes(vars, cmd[3])
        
        elif cmd[0] == "calc":
            #set variable to result
            vars[cmd[4]] = calculate(cmd, vars)

def tokenize():
    with open("test.is") as f:
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

def parse():
    ast = []
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
        else:
            raise Exception("Unknown command: {}".format(token[0]))
    

    return ast

execute()