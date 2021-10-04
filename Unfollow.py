import time
import os
from termcolor import colored
from InstagramAPI import InstagramAPI


def getTotalFollowers(api, user_id):
    """
    Returns the list of followers of the user.
    It should be equivalent of calling api.getTotalFollowers from InstagramAPI
    """

    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers


def getTotalFollowings(api, user_id):
    """
    Returns the list of followers of the user.
    It should be equivalent of calling api.getTotalFollowers from InstagramAPI
    """
    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowings(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers


def nonFollowers(followers, followings):
    nonFollowers = {}
    dictFollowers = {}
    for follower in followers:
        dictFollowers[follower['username']] = follower['pk']

    for followedUser in followings:
        if followedUser['username'] not in dictFollowers:
            nonFollowers[followedUser['username']] = followedUser['pk']

    return nonFollowers

def unFollow(u,p):
    api = InstagramAPI(u,p)
    api.login()
    user_id = api.username_id
    followers = getTotalFollowers(api, user_id)
    following = getTotalFollowings(api, user_id)
    nonFollow = nonFollowers(followers, following)
    totalNonFollowers = len(nonFollow)
    z = 'Number of followers:', len(followers)
    y = 'Number of followings:', len(following)
    x = 'Number of nonFollowers:', len(nonFollow)
    print(colored(z,'blue'))
    print(colored(y,'blue'))
    print(colored(x,'blue'))

    num = len(nonFollow)
    count = num+1
    print('')

    for i in range(num):
        if i >= totalNonFollowers:
            print(colored("[-] Unfollowed All Users Who Were Not Following You Back...:)",'blue'))
            time.sleep(2.5)
            break
        user = list(nonFollow.keys())[len(nonFollow) - 1]
        api.unfollow(nonFollow[user])
        nonFollow.pop(user)
        count = count-1
        message = '[+] Unfollowed - ',count,'('+user+')'
        print(colored(message,'green'))
        time.sleep(7.5)

os.system('cls')
u = input(colored("Enter Username: ",'green'))
p = input(colored("Enter Password: ",'green'))
os.system('cls')

unFollow(u,p)
