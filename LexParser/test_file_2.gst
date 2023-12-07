str:ip_address = input()
int:port
int:port_final
foreach port_initial = 1 to port_final = 444{
    if scanhost(ip_address,port) == "open"{
       show(port)
    }
}
