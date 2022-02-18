static _POG_WHITESPACE: &str = " ";
fn main() {
let mut number = String::new();
std::io::stdin().read_line(&mut number).expect("Failed to read from stdin");
let number: i32 = number.trim().parse().expect("Error parsing number");
if number < 10 {
print!("Number is less than 10");
print!("\n");
}
else {
if number == 10 {
print!("Number is 10");
}
else {
print!("Number is more than 10");
}
print!("\n");
}
}
