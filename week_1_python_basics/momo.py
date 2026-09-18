"""
MTN MoMo balance check simulation.

Reproduces the *170# USSD flow for checking a MoMo wallet balance:
    Main menu -> 6) My Wallet -> 1) Check Balance -> enter PIN -> balance

Zaptek Internship, Week 1.
"""

# PIN is compared as a string, not an int: converting would drop leading
# zeros and let "2345.0" through. A PIN is an identifier, not a quantity.
MOMO_PIN = "2345"

# Stored in pesewas (integer) to avoid float rounding errors on money.
# Divided by 100 only at display time.
MOMO_BALANCE = 100000

MAX_ATTEMPTS = 3

# Menu text transcribed from a live *170# session, 17 Sep 2026.
# "Financial Services" arrives split across two USSD screens because of the
# gateway's character limit; it is one menu item, so it is merged here.
MAIN_MENU = [
    "Transfer Money",
    "MoMoPay&Pay Bill",
    "Airtime&Bundles",
    "Allow Cash Out",
    "Financial Services",
    "My Wallet",
    "Just4U(Offers for you)",
    "MoMo App (300MB free data)",
]

# Same as above: "Change & Reset PIN" is split across screens in the real menu.
WALLET_MENU = [
    "Check Balance",
    "Allow Cash Out",
    "My Approvals",
    "Report Fraud",
    "Statements",
    "Change & Reset PIN",
    "Upgrade Profile Type",
    "Reversals",
    "Check Wallet Limits",
    "Favorite",
    "Name & Next of Kin",
    "Reactivate Wallet",
]


def verify_pin(pin):
    """Return True if the given PIN matches the account PIN."""
    return pin == MOMO_PIN


def is_valid_pin_format(pin):
    """Return True if the PIN is exactly four digits."""
    return pin.isdigit() and len(pin) == 4


def format_balance(pesewas):
    """Convert a balance in pesewas to a display string, e.g. '1,000.00'."""
    return f"{pesewas / 100:,.2f}"


def display_menu(title, items):
    """Print a titled menu, numbering the items from 1."""
    print(f"-----------{title}--------------")
    for index, item in enumerate(items):
        print(f"{index + 1}) {item}")


def get_menu_choice(items):
    """Prompt until a valid option is chosen. Returns a 0-based list index."""
    while True:
        choice = input("Enter option: ").strip()

        if not choice.isdigit():
            print("Enter a digit")
            continue

        if not 1 <= int(choice) <= len(items):
            print("Choice is out of range!")
            continue

        # Menu options are 1-based on screen, lists are 0-based in Python.
        # This is the only place that conversion happens.
        return int(choice) - 1


def check_balance():
    """Ask for the PIN and show the balance, blocking after repeated failures."""
    attempt = 0

    while attempt < MAX_ATTEMPTS:
        entered_pin = input("Enter your MoMo PIN: ").strip()

        # Malformed input does not count as an attempt - the real USSD keypad
        # would not accept it in the first place.
        if not is_valid_pin_format(entered_pin):
            print("Invalid PIN. PIN must be 4 digits!")
            continue

        if verify_pin(entered_pin):
            print(f"Your MoMo balance is GHS {format_balance(MOMO_BALANCE)}")
            break

        attempt += 1
        attempts_left = MAX_ATTEMPTS - attempt

        if attempts_left > 0:
            print(f"Entered PIN is incorrect. {attempts_left} attempt(s) left")
    else:
        # Runs only if the loop ended without break, i.e. all attempts failed.
        print(f"Wrong PIN entered {MAX_ATTEMPTS} times. Your wallet has been blocked.")


def wallet_menu():
    """Show the My Wallet menu and route to the chosen service."""
    display_menu("Wallet Menu", WALLET_MENU)
    index = get_menu_choice(WALLET_MENU)

    if index == 0:
        check_balance()
    else:
        print("Service not available in this simulation.")


def main():
    """Show the main menu and route to the chosen service."""
    display_menu("MoMo", MAIN_MENU)
    index = get_menu_choice(MAIN_MENU)

    if index == 5:
        wallet_menu()
    else:
        print("Service not available in this simulation.")


if __name__ == "__main__":
    main()