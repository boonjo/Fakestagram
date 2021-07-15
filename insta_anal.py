import instaloader
import getpass
import time

start_time = time.time()

USER = input("Enter your Instagram username: ")
PASSWORD = getpass.getpass("Enter your Password: ")

password_length = len(PASSWORD)
password_hide = ('*' * password_length)

access = instaloader.Instaloader()
access.login(USER, PASSWORD)

print("\n⏳ Now searching for all your fake friends... ⌛️\n")

profile = instaloader.Profile.from_username(access.context, USER)

my_followers = []
my_following = []
print("⏳ Now actively judging who you follow... ⌛️\n")
for followee in profile.get_followees():
    my_following.append(followee.username)

print("⏳ Now trying to figure out who would follow you... ⌛️\n")
for followers in profile.get_followers():
    my_followers.append(followers.username)
    
fake_friends = list(set(my_following)-set(my_followers))

if len(fake_friends) == 0:
    print("🎉 Congrats, You have no fake friends 🎉")
else:
    print ("🚨 YOU HAVE " + str(len(fake_friends)) + " FAKE FRIENDS 🚨\n")
    for fake in fake_friends:
        print("💀 " + fake + "\n")
    
print("--- %s seconds ---" % (time.time() - start_time))