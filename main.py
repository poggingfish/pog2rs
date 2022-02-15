import os
with open('out.rs',"w") as f:
    f.write("fn main() {")
    vars={}
    with open('code.pog') as code:
        for x in code.readlines():
            x = x.split()
            command = x[len(x)-1]
            if command == "print":
                try:
                    length = vars[x[0]]["length"]
                except:
                    length = -1
                if x[0] not in vars and len(x) != length:
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
                    if x[0] == "mut":
                        f.write(f'let mut {x[1]}="{x[2]}";')
                    else:
                        f.write(f'let {x[0]}="{x[1]}";')
                if x[0] == "mut":
                    vars.update({
                    x[1]:{
                        "length": 3
                    }
                    })
                else:
                    vars.update({
                    x[0]:{
                        "length": 2
                    }
                    })
            elif command == "add":
                f.write(f"{x[0]}+={x[1]};")
            elif command == "sub":
                f.write(f"{x[0]}-={x[1]};")
            elif command == "if":
                f.write(f"if {x[0]} == {x[1]}"+" {")

            elif command == "end":
                f.write("}")
            elif command == "while":
                if x[1] == "=":
                    f.write(f"while {x[0]} == {x[2]}"+" {")
                if x[1] == ">":
                    f.write(f"while {x[0]} > {x[2]}"+" {")
                if x[1] == "<":
                    f.write(f"while {x[0]} < {x[2]}"+" {")
    f.write("}")
print("Transpile finished.")
print("Compiling")
os.system("rustc out.rs")
print("Running")
print("-------")
os.system("./out")
