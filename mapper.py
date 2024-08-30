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


        except ValueError: 
            print("ERROR: Could not read IP of 'target' file, requried format is 0.0.0.0")
            print("CONSOLE: Finished!")
            exit()

    except Exception as e:
    
        print("ERROR: Could not find a file named 'target'.")

       

        while True:
            create_target_prompt = input ("CONSOLE: Would you like to create a target file?: ")

            if create_target_prompt in ["yes", "y"]:
                new_target = input("Please enter an IP address: ").strip()

                try:
                    ipaddress.ip_address(new_target)
                    os.system(f"echo '{new_target}' > target")
                    return None

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
    target = str(target)
    folder = 'scans'
    existing_dir = os.path.isdir(folder)
    if existing_dir == True: 
        pass

    elif existing_dir == False: 
        try: 
            os.mkdir(folder)

        except Exception as e:
            print("ERROR: Error creating new directoy 'scans'.")
            return


    ### Executes nmap scans. 
    os.system(f"sudo nmap -iL {target} -oN scans/std.map")
    print("CONSOLE: Standard mapping SUCCESS, results available in 'scans/std.map'")

    os.system(f"sudo nmap -sS -sC -sV -Pn -p- -iL {target} -oN scans/adv.map")
    print("CONSOLE: Advance map SUCCESS, results available in 'scans/adv.map'")
    ###

    while True: 
        udp_prompt = input("CONSOLE: Would you like to complete a UDP NMAP?: ")
        if udp_prompt in ["yes", "y"]:
            os.system(f"sudo nmap -sU -iL {target} -oN scans/udp.map")
            print("CONSOLE: UDP mapping SUCCESS, results available in 'scans/adv.map'")

        elif udp_prompt in ["no", "n"]:
            break

        else: 
            print("CONSOLE: Please enter 'yes' or 'no'.")


target = check_target()
print("target value: ", target)
print("target type: ", type(target))

if target == None:
    target = check_target()
    

else:
    auto_map(target)
    
print("CONSOLE: Finished!")
