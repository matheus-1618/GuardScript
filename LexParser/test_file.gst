str:file_name = "ryuk.exe" 
rule:rules_ryuk {
 str:a = ".php?",
 str:b = "uid=",
 str:c = "&uname=",
}
if match(file_name, rules_ryuk){
  show("Arquivo suspeito")
} else{
  show("Arquivo normal")
}
str:ip_address = input()
int:port
int:port_final
foreach port_initial = 1 to port_final = 444{
    if scanhost(ip_address,port) == "open"{
       show(port)
    }
}
int:count = 0
while count < 10000{
  traffic_information()
  count = count + 1
  count = count + 2*count  + 1
}