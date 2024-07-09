import random,string
print("".join(random.choice(string.ascii_uppercase) for _ in range(6)))