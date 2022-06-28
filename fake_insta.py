import sys
import subprocess
import time
import getpass

import instaloader
from alive_progress import alive_bar
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format

imports = ["instaloader", "alive-progress", "pyfiglet", "termcolor", "colorama"]

for im in imports:
    if im in sys.modules is False:
         subprocess.check_call([sys.executable, '-m', 'pip', 'install', im])


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
        return fake_friends
    
def main():    
    subprocess.run("clear")
    cprint(figlet_format('fakestagram', font='speed'), 'blue')
    
    USER = input("Enter your Instagram username: ")
    PASSWORD = getpass.getpass("Enter your Password: ")

    user = InstaUser(USER, PASSWORD)
                    
    print(user.getFake())

if __name__ == "__main__":
    main()