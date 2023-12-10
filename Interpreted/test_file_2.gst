show("Digite o endereço de ip para verificar: ")
str:ip_address = input()
int:port_initial
int:port_final
int:port = 442
foreach port_initial = 442 to port_final = 445{
    if scanhost(ip_address,port) == "open"{
       show("Porta aberta: ")
       show(port)
    } else{
       show("Porta fechada: ")
       show(port)
    }
    port = port + 1
}

