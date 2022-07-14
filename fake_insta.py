import sys
import subprocess
import getpass
import os

import instaloader
from alive_progress import alive_bar
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format

imports = ["instaloader", "alive-progress", "pyfiglet", "termcolor", "colorama"]

class InstaUser:
    def __init__(self, username, password):        
        self.username = username
        self.password = password
        self.access = instaloader.Instaloader()
        self.access.login(self.username, self.password)
        self.profile = instaloader.Profile.from_username(self.access.context, self.username)
        
        self.followers = []
        self.following = []
        
        with alive_bar(self.profile.get_followers().count, title="Looking through your followers") as bar:
            for followers in self.profile.get_followers():
                self.followers.append(followers.username)
                bar()
                
        print("\n")
        
        with alive_bar(self.profile.get_followees().count, title="Judging who you follow") as bar: 
            for followee in self.profile.get_followees():
                self.following.append(followee.username)
                bar()
            
    
    def getFollowers(self):
        return self.followers
    
    def getFollowing(self):
        return self.following

    def getFake(self):
        fake_friends = list(set(self.following)-set(self.followers))
        
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