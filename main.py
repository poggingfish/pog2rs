import sys,os
global toinclude
global included
global linenumber
global currentfile
global used
linenumber = 0
used = []
included = []
def transpile(line,file):
    global variables
    global toinclude
    global included
    global currentfile
    global used
    global linenumber
    f = file
    x = line.split()
    command = x[len(x)-1]
    try:
        if sys.argv[2] == "debugcom":
            f.write(f"//file: {currentfile}, line: {linenumber}, {command}")
            if command != "include":
                f.write("\n")
    except:
        pass
    if command == "print":
        try:
            length = variables[x[0]]["length"]
        except:
            length = -1
        if x[0] not in variables and len(x) != length:
            try:
                int(x[0])
                f.write('print!("{}",'+f"{x[0]});")
            except:
                string=""
                for _ in range(len(x)-1):
                    if _ == len(x)-2:
                        string += x[_]
                    else:
                        string += x[_]+" "
                f.write(f'print!("{string}");')
        else:
            f.write('print!("{}",'+f"{x[0]});")
    elif command == "set":
        try:
            try:
                int(x[1])
            except:
                int(x[2])
            if x[0] == "mut":
                f.write(f"let mut {x[1]}={x[2]};")
            else:
                f.write(f"let {x[0]}={x[1]};")
        except:
            string = ""
            length = 0
            for _ in range(len(x)-1):
                if x[0] == "mut": length = 1
                if _ != length:
                    string+=(str(x[_]))
                if _ < len(x)-2 and _ != 0 : string+=" "
            if x[0] == "mut":
                f.write(f'let mut {x[1]}="{string}";')
            else:
                f.write(f'let {x[0]}="{string}";')
        if x[0] == "mut":
            variables.update({
            x[1]:{
                "length": 3
            }
            })
        else:
            variables.update({
            x[0]:{
                "length": 2
            }
            })
    elif command == "add":
        f.write(f"{x[0]}+={x[1]};")
    elif command == "sub":
        f.write(f"{x[0]}-={x[1]};")
    elif command == "div":
        f.write(f"{x[0]}/={x[1]};")
    elif command == "if":
        f.write(f"if {x[0]} == {x[1]}"+" {")
    elif command == "else":
        f.write("else {")
    elif command == "end":
        f.write("}")
    elif command == "while":
        if x[1] == "=":
            f.write(f"while {x[0]} == {x[2]}"+" {")
        if x[1] == ">":
            f.write(f"while {x[0]} > {x[2]}"+" {")
        if x[1] == "<":
            f.write(f"while {x[0]} < {x[2]}"+" {")
    elif command == "include":
        if x[0] not in included:
            toinclude.append(x[0])
            included.append(x[0])
        else:
            pass
    elif command == "return":
        try:
            int(x[0])
            f.write(f"return {x[0]}")
        except:
            if x[0] in variables:
                f.write(f"return {x[0]}")
            else:
                f.write(f'return "{x[0]}"')
    elif command == "setret":
        print(used)
        print(x)
        if x[0] != "mut":
            used.append(x[1])
            f.write(f"let {x[0]} = {x[1]}(")
            variables.update({
                x[0]:{
                    "length": 2
                }
            })
        else:
            used.append(x[2])
            f.write(f"let mut {x[1]} == {x[2]}(")
            variables.update({
            x[0]:{
                "length": 3
            }
            })
        iterate = 0
        for _ in x:
            if x[0] == "mut":
                length_of = 4
            else:
                length_of = 3
            if len(x) == length_of:
                pass
            else:
                if x[0] == "mut": length=3
                else: length=2
                if iterate >= length and iterate != len(x)-1 and _ != x[0]:
                    if _ in variables:
                        f.write(_+",")
                    else:
                        try:
                            int(_)
                            f.write(_+",")
                        except:
                            f.write(f'"{_}",')
                iterate+=1
        f.write(");")
    else:
        iterate = 0
        used.append(command)
        f.write(f"{command}(")
        for _ in x:
            if iterate != len(x)-1:
                if _ in variables:
                    f.write(_)
                else:
                    try:
                        int(_)
                        f.write(_)
                    except:
                        f.write(f'"{_}"')
            iterate+=1
        f.write(");")
    f.write("\n")
with open('out.rs',"w") as f:
    with open(sys.argv[1]) as code:
        linenumber = 0
        currentfile = code.name
        variables = {}
        macros = {}
        toinclude = []
        #f.write("#![allow(warnings)]\n")
        f.write("fn main() {\n")
        for x in code.readlines():
            linenumber+=1
            transpile(x,f)
        f.write("}\n")
        for x in toinclude:
            for _ in x:
                iterate=0
                if iterate != 0 and iterate<len(x)-1:
                    string+=x[iterate]+" "
                iterate+=1
            with open(x) as include:
                for x in toinclude:
                    with open(x) as includefile:
                        currentfile = includefile.name
                        linenumber = 0
                        for _ in includefile.readlines():
                            linenumber+=1
                            _unsplit = _
                            _=_.split()
                            command=_[len(_)-1]
                            if command == "macro":
                                currentmac = _[0]
                                if currentmac in used:
                                    macvar = []
                                    f.write(f"fn {_[0]}(")
                                    iterate = 0
                                    for variter in _:
                                        if iterate != 0 and iterate != len(_)-1:
                                            macvar.append(_[iterate])
                                        iterate+=1
                                    macros.update({
                                        x[0]:{
                                        "vartypes": macvar
                                        }})
                                    ret=False
                                    macvar=[]
                                    for variter in macros[x[0]]["vartypes"]:
                                        if variter == "int":
                                            f.write("i32")
                                            if ret != True:
                                                f.write(",")
                                        elif variter == "str":
                                            f.write("&str")
                                            if ret != True:
                                                f.write(",")
                                        elif variter == "ret":
                                            f.write(") -> ")
                                            ret = True
                                        elif variter == "noret":
                                            f.write(")")
                                        else:
                                            variables.update({
                                            variter:{
                                                "length": 2
                                            }})
                                            f.write(f"{variter}: ")
                                    f.write("{\n")
                            elif command == "endmac":
                                if currentmac in used:
                                    f.write("}\n")
                            else:
                                try:
                                    if currentmac in used:
                                        transpile(_unsplit,f)
                                except:
                                    transpile(_unsplit,f)
                toinclude.remove(x)

print("Compiling")
os.system("rustc out.rs")
print("Running")
print("-------")
os.system("./out")
