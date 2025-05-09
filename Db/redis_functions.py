
from common_imports import *
r = redis.Redis(host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD,username=REDIS_USERNAME,decode_responses=True)



def adding_user_to_redis(username:str, password:str)->int|None:
    a =1
    users_data = r.get('users_table')
    

    if users_data is None:
        my_list = []
    else:
        my_list = json.loads(users_data)

    for user in my_list:
        a+=1
        if user['username'] == username:
            print("User already exists.")
            return None 

    new_user = {'username': username, 'password': password,"userId":a}
    my_list.append(new_user)
    
    serialized_list = json.dumps(my_list)
    r.set('users_table', serialized_list)
    print(f"User {username} added successfully.")
    return a


def get_user_details(username:str,password:str) ->int|str:
    
    users_data = r.get('users_table')
    users_data= json.loads(users_data)
    for user in users_data:
        if user['username'] == username:
            if user['password']==password:
                return user['userId']
            else:
                return "Incorect Password" 
        
    return "User Not Found"



print(get_user_details("sasa","sa"))