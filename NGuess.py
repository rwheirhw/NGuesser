import random

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print('Please enter a valid integer.')


def choose_mode():
    print('Welcome to NGuess! Specify a range and guess which number was generated to win!!')
    print('Select mode:\n1. Easy\n2. Medium\n3. Hard')
    while True:
        mode = get_int('Enter mode (1-3): ')
        if mode in (1, 2, 3):
            return mode
        print('Please choose 1, 2 or 3.')


def play():
    mode = choose_mode()
    guesses_map = {1: 20, 2: 10, 3: 5}
    max_guesses = guesses_map[mode]
    print(f'You get {max_guesses} guesses for whatever range you pick.\nBest of luck!!')

    while True:
        l_b = get_int('Specify your lower bound: ')
        u_b = get_int('Specify your upper bound: ')
        if l_b < u_b:
            break
        print('Lower bound must be less than upper bound. Please enter the bounds again.')

    to_guess = random.randint(l_b, u_b)
    guesses_left = max_guesses
    attempts = 0
    range_size = u_b - l_b + 1

    while guesses_left > 0:
        print(f'Guesses left: {guesses_left}')
        guessed = get_int('Enter your guess: ')
        attempts += 1

        if guessed == to_guess:
            print(f'You guessed it right!! The number was {to_guess}. You got the answer in {attempts} attempt(s).')
            return

        # Provide a helpful hint
        diff = abs(guessed - to_guess)
        if diff >= range_size * 0.5:
            heat = 'VERY COLD'
        elif diff >= range_size * 0.2:
            heat = 'COLD'
        elif diff >= max(1, range_size * 0.05):
            heat = 'WARM'
        else:
            heat = 'QUITE HOT'

        direction = 'higher' if guessed < to_guess else 'lower'
        print(f'Your guess is {heat}. Try {direction}.')

        guesses_left -= 1

    print(f'You ran out of guesses. Better luck next time. The number was {to_guess}.')


if __name__ == '__main__':
    play()

