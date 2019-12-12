PASSWORD = '12345'


def password_required(func):
    def wrapper():
        password = input('What is your password? ')

        if(password == PASSWORD):
            return func()
        else:
            print('Wrong password')
    return wrapper


@password_required
def needs_password():
    print('Correct password')


def upper(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper


@upper
def say_my_name(name):
    return 'Hello {}'.format(name)


if __name__ == "__main__":
    needs_password()
    print(say_my_name('Ricardo'))
