MOMO_PIN = "2345"
# Balance in pesewas
MOMO_BALANCE = 100000

user_pin = input("Enter your MoMo PIN: ")
if user_pin.strip() == MOMO_PIN:
    print(f"Your MoMo balance is GHS {MOMO_BALANCE//100:,.2f}")
else:
    print("Entered pin is incorrect")