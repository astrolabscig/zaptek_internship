MOMO_PIN = "2345"
# Balance in pesewas
MOMO_BALANCE = 100000
MAX_ATTEMPTS = 3

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
    return pin == MOMO_PIN

def is_valid_pin_format(pin):
    return pin.isdigit() and len(pin) == 4

def format_balance(pesewas):
    return f"{pesewas/100:,.2f}"

def display_menu(title, items):
    print(f"-----------{title}--------------")
    for index, item in enumerate(items):
        print(f"{index + 1}) {item}")

def get_menu_choice(items):
    while True:
        choice = input("Enter option: ").strip()
        if not choice.isdigit():
            print("Enter a digit")
            continue
        if not 1 <= int(choice) <= len(items):
            print("Choice is out of range!")
            continue
        return int(choice) - 1

def check_balance():
    attempt = 0

    while attempt < MAX_ATTEMPTS:
        entered_pin = input("Enter your MoMo PIN: ").strip()

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
        print(f"Wrong PIN entered {MAX_ATTEMPTS} times. Your wallet has been blocked.")

def wallet_menu():
    display_menu("Wallet Menu", WALLET_MENU)
    index = get_menu_choice(WALLET_MENU)
    if index == 0:
        check_balance()
    else:
        print("Service not available in this simulation.")


def main():

    display_menu("MoMo",MAIN_MENU)
    index = get_menu_choice(MAIN_MENU)

    if index == 5:
        wallet_menu()
    else:
        print("Service not available in this simulation.")


   



if __name__ == "__main__":
    main()