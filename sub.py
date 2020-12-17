from colorama import Fore, Back, init
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
import datetime
import getpass
# import pandas as pd
import re

time_now = datetime.datetime.now().isoformat(timespec="seconds").replace(":", "-")
last_char_index = time_now.rfind("T")
time_now = time_now[:last_char_index] + "_" + time_now[last_char_index + 1:]

# Initialize colorama and reset style by default
init(autoreset=True)


def read_from_filename(filename):
    # Filename гэх файлын мөр бүрийг буцаах
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


def get_credentials():
    # username, password-г хэрэглэгчээс авах
    username = "display-domain"
    password = "EneNuutsUgNiShuu123$%^KeepItSecret"
    return username, password


def connect_and_send(devices_lines, config_lines, username, password):
    # Төхөөрөмжтэй холбогдож өгөгдсөн командыг хийдэг функц
    for ip in devices_lines:
        device = {
            "device_type": "huawei",
            "ip": ip,
            "username": username,
            "password": password
        }
        try:
            print(Fore.MAGENTA + "=" * 70)
            print(Fore.CYAN + "" * 15 + " Connecting to Device: " + ip)
            print(Fore.MAGENTA + "=" * 70)
            net_connect = ConnectHandler(**device)

            # "display current-configuration configuration system | include sysname"
            # Huawei-н төхөөрөмж бол sysname-р нь файлыг хадгалах
            if (ip == "192.168.250.58"):
                hostname = "BRAS#1"
            elif (ip == "192.168.250.57"):
                hostname = "BRAS#2"
            elif (ip == "192.168.250.8"):
                hostname = "BRAS#3"
            elif (ip == "192.168.250.9"):
                hostname = "BRAS#4"
            else:
                hostname = "unknown"

            filename = hostname + "_" + time_now + ".txt"

            print(Fore.GREEN + "~" * 70)
            print(Fore.CYAN + "" * 15 + " Connected to Device: " + ip + " " + hostname)
            print(Fore.CYAN + "" * 15 + " Sending commands ")
            print(Fore.CYAN + "" * 15 + " Saving output to: " + hostname + "_" + time_now)
            print(Fore.GREEN + "~" * 70)
            # Open file to write to
            # filename = ip + "_" + time_now + ".txt"
            with open(filename, "w+") as f:
                for command in config_lines:
                    cmd_output = net_connect.send_command(command)

                    # f.write(re.sub("  ", "\t", cmd_output))
                    cmd_output = cmd_output.split("\n", 3)[3]
                    # cmd_output = cmd_output[243:]
                    cmd_output = cmd_output.rsplit("\n", 2)[0]
                    # cmd_output = cmd_output[:-103]

                    # matched_lines = search_multiple_strings_in_file(filename, ['is', 'what'])

                    f.write(cmd_output)
                f.close()
            with open(filename, "r+") as f:
                new_f = f.readlines()
                f.seek(0)
                for line in new_f:
                    if ("default" not in line) and ("enterprise-" not in line) and ("internet_" not in line):
                        f.write(line)
                f.truncate()

            # read_file = pd.read_csv(filename, sep='\t')
            # read_file.head()
            # read_file.to_csv (hostname+"_"+time_now+".csv", index=None)


        except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
            print(Fore.RED + "~" * 15 + str(e) + "~" * 15)


if __name__ == "__main__":
    # Текст файлаас командуудыг авна
    config_lines = read_from_filename("commands.txt")
    # Текст файлаас холбогдох төхөөрөмжүүдийн хаягыг авна
    devices_lines = read_from_filename("devices.txt")
    # Username, password-г авна
    username, password = get_credentials()
    # Төхөөрөмжүүдтэй холбогдож командуудын үр дүнг цуглуулж файл дээр цуглулна
    connect_and_send(devices_lines, config_lines, username, password)