from datetime import datetime, timedelta

class PaymentProcessor:

    @staticmethod
    def authenticate_paypal(email, password):
        '''The function creates a dictionary with the keys email and password, which contains the provided email address and password.'''
        data = {"email": email, "password": password}
        return True

    def is_valid_expiry_date(exp_date_str):
        '''The function checks the expiration date of a credit card'''
        try:
            exp_date = datetime.strptime(exp_date_str, "%m/%Y")
            exp_date = exp_date.replace(day=1)
            next_month = exp_date.month % 12 + 1
            next_month_year = exp_date.year + (exp_date.month // 12)
            exp_date_end = exp_date.replace(month=next_month, year=next_month_year) - timedelta(days=1)
            current_date = datetime.now()
            return current_date <= exp_date_end
        except ValueError:
            return False
