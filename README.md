# pog2rs
## The Rust transpiler for the Pogcode Language  
#### (Written in python)
### Features
- Support for libraries (std.pog, math.pog, color.pog, etc)
- Fast run time since it transpiles to rust
- Easy to learn
### TODO
- [ ] Make main.py code a bit easier to read
- [ ] Comments (Should be fairly easy)
- [ ] Rewrite in something other than python....
- [ ] Self Hosted ( Never gonna happen.... But maybe )
### Usage
Transpiling and running
```
python3 main.py program.pog
rustc program.rs
./program
```
### Examples
Hello world
```
Hello, world! print
\n print
```
Simple math (Should return 5)
```
math.pog include
std.pog include
result retdiv 10 2 setret
result printint
```
If Statements
```
number input
number toint
number < 10 if
Number is less than 10 print
\n print
end
else
Number is more than 10 print
end
```
