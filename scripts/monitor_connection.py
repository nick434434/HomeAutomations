from os import curdir
import sys
# Necessary for pure console usage in Windows
sys.path.append(curdir)

from datetime import datetime
from time import sleep

from requests import get, RequestException

from console.input import NonBlockingConsole
from file.file import File


# 60 measures = slightly more than a minute, enough time to see that the connection doesn't work
NUM_MEASURES = 60
MACHINE_EPSILON = 1e-5
REPORT_INTERVAL = 3500  # 3500 - almost each hour or a bit more frequent than each hour given requests.get() delays


def check_website(website: str):
    try:
        result = get(website, timeout=0.5)
        return result.ok
    except RequestException:
        return False


def check_google():
    return check_website("https://google.com")


def check_wikipedia():
    return check_website("https://wikipedia.org")


if __name__ == "__main__":
    input("Press 'Enter' to start!")
    print(f"Welcome to Connection Monitoring tool! The tool will be reporting connection resets to a file")
    filename = input("Please enter a filename: ")
    print("Press 'q' to quit!")

    running_average = 0
    google_results = [1] * NUM_MEASURES
    wikipedia_results = [1] * NUM_MEASURES

    with File(filename, writeable=True) as file:
        with NonBlockingConsole() as nbc:

            counter = 0

            while True:
                google_check = check_google()
                wikipedia_check = check_wikipedia()

                google_results.append(int(google_check))
                wikipedia_results.append(int(wikipedia_check))

                google_results.pop(0)
                wikipedia_results.pop(0)

                running_average = (sum(google_results) + sum(wikipedia_results)) / (2 * NUM_MEASURES)

                # TODO: date module
                counter = (counter + 1) % REPORT_INTERVAL
                if not counter:
                    file.writeln(f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} - "
                                 f"Successful web checks over last {NUM_MEASURES} checks: {100 * running_average}%")

                if abs(running_average) < MACHINE_EPSILON:
                    file.writeln(f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} - "
                                 f"No connection based on last {NUM_MEASURES} checks!")
                    google_results = [1] * NUM_MEASURES
                    wikipedia_results = [1] * NUM_MEASURES

                if nbc.get_q():
                    break

                # Do not make a DDoS attack :D
                sleep(1)
