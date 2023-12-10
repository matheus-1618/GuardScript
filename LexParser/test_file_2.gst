show("Digite o endereço de ip para verificar: ")
str:ip_address = input()
int:port_initial
int:port_final
int:port = 8079
foreach port_initial = 8079 to port_final = 8082{
    if scanhost(ip_address,port) == "open"{
       show("Porta aberta: ")
       show(port)
    } else{
       show("Porta fechada: ")
       show(port)
    }
    port = port + 1
}
