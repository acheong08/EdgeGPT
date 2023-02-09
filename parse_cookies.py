cookies = {}
with open("cookies.txt") as f:
    cookies = f.read().split("; ")
    # Everything after the first "=" is the value (there may be multiple =)
    cookies = {
        cookie.split("=")[0]: "=".join(cookie.split("=")[1:]) for cookie in cookies
    }

print(cookies)
