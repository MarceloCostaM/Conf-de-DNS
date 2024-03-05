#!/usr/bin/python3
import argparse
import subprocess

def config_de_zonaD(dominio):
    named_conf_file = '/etc/bind/named.conf.default-zones'
    with open(named_conf_file, 'a') as conf_file:
        conf_file.write(f"zone \"{dominio}\" {{\n"
                        f"    type master;\n"
                        f"    file \"/etc/bind/db.{dominio}\";\n"
                        f"}};\n")

    zona_file_path = f'/etc/bind/db.{dominio}'
    with open(zona_file_path, 'w') as zona_file:
        zona_file.write(f";\n"
                        f"; BIND data file for {dominio}\n"
                        f";\n"
                        f"$TTL  604800\n"                
                        f"@   IN  SOA {dominio}. root.{dominio}. (\n"
                        f"              2         ; Serial\n"
                        f"         604800         ; Refresh\n"
                        f"          86400         ; Retry\n"
                        f"        2419200         ; Expire\n"
                        f"         604800 )       ; Negative cash TTL\n"
                        f"\n"                       
                        f"@   IN  NS  nome.{dominio}.\n"                                  
                        f"nome IN  A   192.168.10.15\n"
                        f"www  IN  A   192.168.10.20\n"
                        f"ftp  IN  CNAME   www.{dominio}.\n"
                        f"smtp  IN  CNAME   www.{dominio}.")

def config_de_zonaR(reverse_ip, dominio):
    named_conf_file = '/etc/bind/named.conf.default-zones'
    with open(named_conf_file, 'a') as conf_file:
        conf_file.write(f"zone \"{reverse_ip}.in-addr.arpa\" {{\n"
                        f"         type master;\n"
                        f"         file \"/etc/bind/db.{reverse_ip}\";\n"
                        f"}};\n")

    zona_file_path = f'/etc/bind/db.{reverse_ip}'
    with open(zona_file_path, 'w') as zona_file:
        zona_file.write(f";\n"
                        f"; BIND data file for {reverse_ip}\n"
                        f";\n"                        
                        f"$TTL 604800\n"
                        f"@ IN  SOA {dominio}. root.{dominio}. (\n"
                        f"              2         ; Serial\n"
                        f"         604800         ; Refresh\n"
                        f"          86400         ; Retry\n"
                        f"        2419200         ; Expire\n"
                        f"          86400 )       ; Negative Cache TTL\n"
                        f"\n"                       
                        f"@    IN  NS  nome.{dominio}.\n"
                        f"13   IN  PTR nome.{dominio}.\n"
                        f"13   IN  PTR  www.{dominio}.\n"
                        f"13   IN  PTR  smtp.{dominio}.\n"
                        f"13   IN  PTR  ftp.{dominio}.\n")

def reiniciar_bind():
    subprocess.run(['service', 'named', 'restart'])

def main():
    parser = argparse.ArgumentParser(description="Configurar um servidor DNS BIND")
    parser.add_argument("--zonadireta", "-zd", help="Configurar zona direta para o domínio especificado")
    parser.add_argument("--zonareversa", "-zona", help="Configurar zona reversa para o IP reverso especificado")
    parser.add_argument("--stop", help="Parar o serviço BIND", action="store_true")
    parser.add_argument("--start", help="Iniciar o serviço BIND", action="store_true")
    parser.add_argument("--status", help="Verificar status do serviço BIND", action="store_true")

    args = parser.parse_args()

    if args.zonadireta:
        config_de_zonaD(args.zonadireta)

    if args.zonareversa:
        config_de_zonaR(args.zonareversa, args.zonadireta)

    if args.stop:
        subprocess.run(['named', 'systemctl', 'stop'])

    if args.start:
        subprocess.run(['named', 'systemctl', 'start'])

    if args.status:
        subprocess.run(['named', 'systemctl', 'status'])

    if args.zonadireta or args.zonareversa:
        reiniciar_bind()

if __name__ == "__main__":
    main()