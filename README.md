
# ATM

### Clone
git clone https://github.com/Godrl/atm.git


### Run
python3 controller.py in the command line

### Detail

- Bank Class
  - Bank constructor
  - Create an account for your card using the 'create_account' method
  - Add an account for your card using the 'add_account' method
  - Verify that the pin is correct using the 'check_pin_num' method
  - Change your account balance using the 'update_account' method
  
- Controller Class
  - Constructor takes in a Bank object and dollar
  - Verify that your account is valid using the 'swipe' method
  - Check that the account selected by the user is valid through 'account_select' method.
  - Account actions method is the way balance/withdraw/deposit are implemented
  - call function is the basic driver of the controller.
