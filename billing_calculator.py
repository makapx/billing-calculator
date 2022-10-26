import argparse  # argument parser
import re  # regex to validate roommate input
import time  # time library

# ANSI color codes
SHELL_CYAN = "\033[96m"
SHELL_GREEN = "\033[92m"
SHELL_RESET = "\033[0m"


class Roommate:
    # constructor
    def __init__(self, name: str, days_at_home: int):
        self.name = name
        self.days_at_home = days_at_home

    # override the default string representation of the object
    def __repr__(self):
        return f"{self.name}:{self.days_at_home}"

    # def __eq__(self, __o: object) -> bool:
    #    pass


# TODO pick up a type for type, start_date, end_date
# TODO print roommates in a nice way
class Bill:
    def __init__(
        self, type, amount: float, start_date, end_date, roommates: list[Roommate]
    ):
        self.type = type
        self.amount = amount
        self.start_date = start_date
        self.end_date = end_date
        self.roommates = roommates

    def __repr__(self):
        return f"{self.type} {self.amount} {self.start_date} {self.end_date} {self.roommates}"


def calculator(roommates: list[Roommate], total_amount: float):
    print("Calculating bills...")
    time.sleep(1)  # pretend to do some calculations

    total_days = 0

    # calculate total days at home for all roommates
    for roommate in roommates:
        total_days += roommate.days_at_home

    # handle no roommates at home case
    if total_days == 0:
        total_amount_per_person = total_amount / len(roommates)
        print(
            f"No one is at home, we split the bill equally: {total_amount_per_person:.2f}€ per person"
        )
        return

    # calculate the amount each roommate has to pay and print it out in a nice way
    for roommate in roommates:
        bill = roommate.days_at_home / total_days * total_amount
        print(f"{SHELL_CYAN}{roommate.name}{SHELL_RESET} pays: {bill:.2f}€")

    # print the total amount
    print(f"{SHELL_GREEN}Total: {total_amount:.2f}€{SHELL_RESET}")


def validate_roommate_regex(
    arg_value: str,
    pat=re.compile(r"^[a-zA-Z]{1,25}:\d{1,3}$"),
):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError(
            "Invalid format. Expeted [name]:[days_at_home]"
        )

    # split the string by the colon and create a new Roommate object for each one
    name, days_at_home = arg_value.split(":")
    return Roommate(name, int(days_at_home))


def register_new_bill(bill: Bill):
    status = open("billsHistory.txt", "a").write(str(bill) + "\n")

    # check if write was successful, if not, raise exception
    if status == 0:
        raise Exception("Error writing to file")

    print(f"{SHELL_GREEN}Bill registered successfully!{SHELL_RESET}")


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--roommate",
        help="Add new roommate to roommates list. Format [name]:[days_at_home]",
        nargs="+",
        type=validate_roommate_regex,
    )

    parser.add_argument(
        "-t", "--total_amount", help="Total bills amount", required=True, type=float
    )

    args = parser.parse_args()

    calculator(args.roommate, args.total_amount)

    print("Do you want to add a new bill? (y/n)")

    # TODO add validation for inputs
    answer = input()
    if answer == "y":
        print("Please enter the bill type")
        bill_type = input()
        print("Please enter the bill start date")
        bill_start_date = input()
        print("Please enter the bill end date")
        bill_end_date = input()

        bill = Bill(
            bill_type,
            float(args.total_amount),
            bill_start_date,
            bill_end_date,
            args.roommate,
        )
        register_new_bill(bill)


if __name__ == "__main__":
    main()
