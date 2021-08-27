def make_repeater_of(n):
    def repeater(string):
        assert type(string) == str, 'Solo puedes repetir cadenas'
        return string * n
    return repeater

def make_division_by(n):
    def divisor(number):
        assert type(number) == int or type(number) ==float, 'Solo puedes dividir enteros'
        return number / n
    return divisor

def run():
    repeat_5 = make_repeater_of(5)
    divisor_10 = make_division_by(10)
    print(repeat_5('Hola'))
    print(divisor_10(4))


if __name__ == '__main__':
    run()


    