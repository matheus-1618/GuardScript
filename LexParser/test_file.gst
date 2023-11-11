str:ip = input() // for example: 192.168.12.5
int:port
int:port_final
// for each number since 1 to 443
foreach port_initial= 1 to port_final = 444{
    // scanhost is a built-in function that see if a desired port in a host is open or not
    if scanhost(ip_address,port) {
       show("Porta ")
       show(porta)
       show("Aberta")
    }
}