import requests
import pandas as pd

class vk_user:
    def __init__(self, vk_id, friends):
        self.vk_id = vk_id
        self.friends = friends
        
users = [vk_user(162225997, None)]

deep = 2
for _ in range(deep):
    new_users = []
    for user in users:
        if user.friends == None:
            url = f'https://api.vk.com/method/friends.get?user_id={user.vk_id}&&v=5.199'
            response = requests.get(url)
            if 'response' not in response.json():
                continue
            user.friends = response.json()['response']['items']
            for friend in response.json()['response']['items']:
                if all(person.vk_id != friend for person in users):
                    new_users.append(vk_user(friend, None))
    users.extend(new_users)

friendships = []

for user in users:
    if user.friends == None:
        continue
    for friend in user.friends:
        if (user.vk_id, friend) not in friendships:
            friendships.append((user.vk_id, friend))


df = pd.DataFrame(friendships, columns=['VK_user_1', 'VK_user_2'])
df.to_csv('friendships.csv', index=False)