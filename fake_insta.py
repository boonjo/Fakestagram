import sys
import subprocess
import getpass
from instagrapi import Client
from alive_progress import alive_bar
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format

imports = ["instagrapi", "alive-progress", "pyfiglet", "termcolor", "colorama"]

class InstaUser:
    def __init__(self, username, password):        
        self.username = username
        self.password = password
        self.cl = Client()
        self.cl.login(self.username,  self.password)
        
        self.ID = self.cl.user_id_from_username(self.username)
            
        self.followers = []
        self.following = []

        with alive_bar(len(self.cl.user_followers_v1(self.ID)), title="Looking through your followers") as bar:
            self.user_followers = self.cl.user_followers_v1(self.ID)
            for user in self.user_followers:
                self.followers.append(user.username)
                bar()
                
        print("\n")
        
        with alive_bar(len(self.cl.user_following_v1(self.ID)), title="Judging who you follow") as bar: 
            self.user_following = self.cl.user_following_v1(self.ID)
            for user in self.user_following:
                self.following.append(user.username)
                bar()

    def getFake(self):
        fake_friends = [item for item in self.following if item not in self.followers]
        
        if (len(fake_friends) == 0):
            print("\n\n🎉 Everyone follows you back! 🎉")
            return
        else:
            print("\n\n🚨 These are your fake 'friends' 🚨\n")
            for fake in fake_friends:
                print('💀 {}\n'.format(fake))
            return
    
def main():
    for im in imports:
        if im in sys.modules is False:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', im])
    
    subprocess.run("clear")
    cprint(figlet_format('fakestagram', font='speed'), 'blue')
    cprint("Created by Joonbo Shim\n", 'blue')
    
    USER = input("Enter your Instagram Username: ")
    PASSWORD = getpass.getpass("\nEnter your Instagram Password: ")
    print('\n')

    user = InstaUser(USER, PASSWORD)
                    
    user.getFake()

if __name__ == "__main__":
    main()