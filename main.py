#!/usr/bin/env python3


# Imports
import random
import argparse
from readchar import readkey, key
from colorama import Fore, Back, Style, init
from time import time, ctime
from collections import namedtuple
from pprint import pprint


init(autoreset=True)        # auto reset colorama colors


def args():
    """
    Manage command line arguments
    
    Return:
        use_time_mode: bool, defines ending condition
        max_value: int, if use_time_mode = True, represents number of seconds
                        if use_time_mode = False, represents number of inputs

    """

    parser = argparse.ArgumentParser(description='PSR Typing Test')
    parser.add_argument('-utm', '--use_time_mode', action='store_true', help='Use this argument to play in time mode')
    parser.add_argument('-mv', '--max_value', type=int, required=True, help='Maximum number of inputs / Time mode: maximum number of seconds.')

    args = vars(parser.parse_args())
    max_value = args["max_value"]
    use_time_mode = args["use_time_mode"]

    return use_time_mode, max_value


def main():

    utm, mv = args()

    if utm:
        print("Test running up to", mv, "seconds.")
    else:
        print("Test running up to", mv, "inputs.")

    print(Fore.GREEN + "\nPress any key to start...\n")


    _ = readkey()   # Wait for user input to start


    # Initialize variables
    test_start = time()
    number_of_types = 0
    number_of_hits = 0
    Input = namedtuple('Input', ['requested', 'received', 'duration'])
    inputs = []
    type_average_duration = 0
    type_hit_average_duration = 0
    type_miss_average_duration = 0


    while True:

        # Request a random character from a to z
        requested = chr(random.randint(97,122))

        print("Press:", Fore.CYAN + requested)

        request_time = time()


        # Wait for user input
        received = readkey()


        # Break if the key is SPACE - don't include this input in statistics
        if received == key.SPACE:
            print(Fore.RED + "\nInterrupted by user\n")
            break

        number_of_types += 1

        duration = time() - request_time
        type_average_duration += duration


        # Validate input
        if received == requested:
            number_of_hits += 1
            type_hit_average_duration += duration
            print("You pressed:", Fore.GREEN + received)

        else:
            type_miss_average_duration += duration
            print("You pressed:", Fore.RED + received)


        # Save input in list
        inputs.append(Input(requested, received, duration))


        # Stop conditions
        if utm and (time() - test_start > mv):
            print(Fore.RED + "\nCurrent test duration (" + str(time() - test_start) + ") exceeds maximum of " + str(mv) + " seconds.\n")
            break

        elif not utm and (number_of_types >= mv):
            print(Fore.RED + "\nCurrent number of types (" + str(number_of_types) + ") has reached its maximum value.\n")
            break


    # Statistics
    test_end = time()
    test_duration = test_end - test_start
    accuracy = 0


    # Calculate accuracy and average durations
    if number_of_types != 0:
        accuracy = number_of_hits / number_of_types
        type_average_duration /= number_of_types

    if number_of_hits != 0:
        type_hit_average_duration /= number_of_hits

    if number_of_types - number_of_hits != 0:
        type_miss_average_duration /= (number_of_types - number_of_hits)


    statistics = {'inputs': inputs,
                    'accuracy': accuracy,
                    'number_of_hits': number_of_hits,
                    'number_of_types': number_of_types,
                    'test_duration': test_duration,
                    'test_end': ctime(test_end),
                    'test_start': ctime(test_start),
                    'type_average_duration': type_average_duration,
                    'type_hit_average_duration': type_hit_average_duration,
                    'type_miss_average_duration': type_miss_average_duration}

    pprint(statistics)


if __name__ == "__main__":
    main()