from random import randrange

def summ(a):
    summ = 0
    if (a > 0):
        for i in range(a + 1):
            summ += i
    else:
        for i in range(a, 0):
            summ += i
    return summ

if __name__ == '__main__':
    print(summ(-1))
    print(summ(0))
    print(summ(1))
    with open('2.txt', 'w') as f:
        left = -1 * 10 ** 5
        right = 10 ** 5
        for i in range(100):
            rand = randrange(left, right)
            sm = summ(rand)
            f.write(f'{rand}, {sm}\n')
