# GuardScript

A programming language crafted to aid cybersecurity professionals in their tasks, including:

* Scanning for the presence of malware on a machine.
* Conducting scans of hosts and ports.
* Real-time Network Traffic Analysis.

All of this comes with a straightforward and simple syntax that eases the development of programs designed to assist in cybersecurity defense or investigative environments, centralizing initial analyses in a single language and development environment.

## EBNF
```
PROGRAM = { STATEMENT };

BLOCK = { "{", "\n", STATEMENT, "}"};

STATEMENT = ( λ | ASSIGNMENT | CONDITIONAL| PRINT| FOREACH | WHILE | VAR | RULE | MATCH | SCANHOST | TRAFFIC), "\n" ;

ASSIGNMENT = IDENTIFIER, "=", REXPRESSION;

CONDITIONAL= "if", BEXPRESSION, {"else", BLOCK|BLOCK};

PRINT = "show", "(", BEXPRESSION, ")";

FOREACH = "foreach", ASSIGNMENT, "to", ASSIGNMENT, BLOCK;

WHILE = "while", BEXPRESSION, BLOCK;

VAR = TYPE, ":", IDENTIFIER, {"=", BEXPRESSION};

RULE = "rule", ":", IDENTIFIER, "{", {VAR, ",", "\n"}, "}";

TYPE = (int | str);

MATCH = "match", "(", VAR ,RULE, ")";

SCANHOST = "scanhost", "(", VAR, VAR, ")";

TRAFFIC = "traffic_information", "(", ")";

BEXPRESSION = BTERM, {("||"), BTERM};

BTERM = REXPRESSION, {("&&"), REXPRESSION};

REXPRESSION = EXPRESSION, {("==" | ">" | "<"), EXPRESSION};

EXPRESSION = TERM, {("+" | "-" ), TERM};

TERM = FACTOR, {("*" | "/"), FACTOR };

FACTOR = (("+" | "-" | "!"), FACTOR | INT | STR | "(", EXPRESSION, ")" | IDENTIFIER | INPUT);

IDENTIFIER = LETTER, { LETTER | DIGIT | "_"};

INPUT = "input", "(", ")";

STR = ", {LETTER}+, ";

INT = {NUMBER}+;

NUMBER = DIGIT, { DIGIT };

LETTER = ( a | ... | z | A | .. | Z);

DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
```

## Examples
### Verifying if an executable file is malware or not

For malware analysts, static analysis is a significant part of their work. It involves scanning the characteristics of a file to determine whether the investigated file is a sample of malicious code. Currently, they use Yara Rules, a declarative method for evaluating strings and libraries present in a file. GuardScript incorporates this functionality into the language, simplifying the process.
```go
//Verify if a suspicious file is malware.
str:file_name = "ryuk.exe" //Name of the executable file in  the path

//rule (set of strings to inspect if they are in the suspected file)
rule:rules_ryuk {
 str:a = ".php?",
 str:b = "uid=",
 str:c = "&uname=",
}

//conditional flow
//match is a built in function that returns 1 if the strings are present in executable, and 0 otherwise.
if match(file_name, rules_ryuk){
  show("Arquivo suspeito")
} else{
  show("Arquivo normal")
}
```

### Scanning ports of a host

For security professionals, the process of host reconnaissance is essential and should be automated and quick. GuardScript simplifies this with a straightforward syntax and its own functions.

```go
str:ip_address = input() // for example: 192.168.12.5
int:port
int:port_final
// for each number since 1 to 443
foreach port_initial= 1 to port_final = 444{
    // scanhost is a built-in function that see if a desired port in a host is open or not
    if scanhost(ip_address,port) == "open"{
       show("Porta ")
       show(porta)
       show("Aberta")
    }
}
```

### Real-time Network Traffic Analysis

GuardScript also makes simultaneous traffic monitoring easy, ideal for building real-time monitoring daemons.

```go
int:count = 0
while count < 10000{
  traffic_information() // a built in function that generates logs from traffic in the current host
  count = count + 1
}
```
