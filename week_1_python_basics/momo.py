MOMO_PIN = "2345"
# Balance in pesewas
MOMO_BALANCE = 100000
MAX_ATTEMPTS = 3

def verify_pin(pin):
    return pin == MOMO_PIN

def is_valid_pin_format(pin):
    return pin.isdigit() and len(pin) == 4


def format_balance(pesewas):
    return f"{pesewas/100:,.2f}"


def main():
    attempt = 0
    
    while attempt < MAX_ATTEMPTS:
        entered_pin = input("Enter your MoMo PIN: ").strip()

        if not is_valid_pin_format(entered_pin):
            print("Invalid PIN. PIN must be 4 digits!")
            continue

        if verify_pin(entered_pin):
            print(f"Your MoMo balance is GHS {format_balance(MOMO_BALANCE)}")
            break

        attempt+=1
        attempts_left = MAX_ATTEMPTS - attempt

        if attempts_left > 0:
            print(f"Entered pin is incorrect. {attempts_left} attempt(s) left")
        
    else:
        print(F"Wrong PIN entered {MAX_ATTEMPTS} times. Your wallet has been blocked.")



if __name__ == "__main__":
    main()