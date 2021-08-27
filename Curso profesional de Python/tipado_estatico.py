import time 
def is_palindrome(string: str) -> bool:
    string = string.replace(' ', '').lower()
    return string == string[::-1]


def run():
    time.sleep(2)
    print(is_palindrome(10000))


if __name__ == '__main__':
    run()