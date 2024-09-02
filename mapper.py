import os
import ipaddress

print("""
                         )       )   *           (     
   (            *   ) ( /(    ( /( (  `    (     )\ )  
   )\       ( ` )  /( )\())   )\()))\))(   )\   (()/(  
((((_)(     )\ ( )(_)|(_)\   ((_)\((_)()((((_)(  /(_)) 
 )\ _ )\ _ ((_|_(_())  ((_)   _((_|_()((_)\ _ )\(_))   
 (_)_\(_) | | |_   _| / _ \  | \| |  \/  (_)_\(_) _ \  
  / _ \ | |_| | | |  | (_) | | .` | |\/| |/ _ \ |  _/  
 /_/ \_\ \___/  |_|   \___/  |_|\_|_|  |_/_/ \_\|_| \n""")


def check_target(): 
    try:
        target = open("target","r").read().strip()

        try:
            ipaddress.ip_address(target)
            print(f"CONSOLE: Target set to -> {target}")
            return target


        except ValueError: 
            print("ERROR: Could not read IP of 'target' file, requried format is 0.0.0.0")
            print("CONSOLE: Finished!")
            exit()

    except Exception as e:
    
        print("ERROR: Could not find a file named 'target'.")
    

        while True:
            create_target_prompt = input ("CONSOLE: Would you like to create a target file?: ").strip().lower()

            if create_target_prompt in ["yes", "y"]:
                new_target = input("CONSOLE: Please enter an IP address: ").strip()

                try:
                    ipaddress.ip_address(new_target)
                    os.system(f"echo '{new_target}' > target")
                    return new_target

                except ValueError: 
                    print("ERROR: No valid IP Address in 'target' file, requried format is 0.0.0.0")
                    print("CONSOLE: Invalid target file has not been created.")
                    print("CONSOLE: Finished!")
                    exit()

            elif create_target_prompt in ["no", "n"]:
                print("CONSOLE: Please create a file named 'target' cotaining an IP and rerun.")
                print("CONSOLE: Finished!")
                exit() 

            else:
                print("CONSOLE: Please enter 'yes' or 'no'.")
            

def auto_map(target):
    #targetz = str(target)
    folder = 'scans'
    existing_dir = os.path.isdir(folder)
    if existing_dir == True: 
        pass

    elif existing_dir == False: 
        try: 
            print("CONSOLE: Created new scans folder...")
            os.mkdir(folder)

        except Exception as e:
            print("ERROR: Error creating new directoy 'scans'.")
            return


    ### Executes nmap scans. 
    # STD Map
    while True: 
        std_prompt = input("CONSOLE: Would you like to complete a Standard NMAP?: ").strip()
        if std_prompt.lower() in ["yes", "y"]:
            print("")
            os.system(f"sudo nmap {target} -oN scans/std.map")
            print("CONSOLE: UDP mapping SUCCESS, results available in 'scans/std.map'.\n")

        elif udp_prompt.lower() in ["no", "n"]:
            break

        else: 
            print("CONSOLE: Please enter 'yes' or 'no'.")

    # ADV Map
    while True:
        adv_prompt = input("CONSOLE: Would you like to complete a Advance NMAP?: ").strip()
        if adv_prompt.lower() in ["yes", "y"]:
            print("")
            os.system(f"sudo nmap -sS -sC -sV -Pn -p- {target} -oN scans/adv.map")
            print("CONSOLE: Advance map SUCCESS, results available in 'scans/adv.map'.\n")

        elif udp_prompt.lower() in ["no", "n"]:
            break

        else: 
            print("CONSOLE: Please enter 'yes' or 'no'.")

    # UDP Map
    while True: 
        udp_prompt = input("CONSOLE: Would you like to complete a UDP NMAP?: ").strip()
        if udp_prompt.lower() in ["yes", "y"]:
            os.system(f"sudo nmap -sU {target} -oN scans/udp.map")
            print("CONSOLE: UDP mapping SUCCESS, results available in 'scans/adv.map'")

        elif udp_prompt.lower() in ["no", "n"]:
            break

        else: 
            print("CONSOLE: Please enter 'yes' or 'no'.")


### Program

target = check_target()

if target == None:
    target = check_target()
    auto_map(target)
    

else:
    auto_map(target)
    
print("CONSOLE: Finished!")
