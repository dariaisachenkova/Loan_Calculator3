import argparse
import math

parser = argparse.ArgumentParser(description='Loan Calculator')

parser.add_argument('--type', type=str)
parser.add_argument('--payment', type=int)
parser.add_argument('--interest', type=float)
parser.add_argument('--principal', type=int)
parser.add_argument('--periods', type=int)

TYPE_ALLOWED_VALUES = ['annuity', 'diff']

args = parser.parse_args()

type = args.type
payment = args.payment
interest = args.interest
principal = args.principal
periods = args.periods
arg_lst = [arg for arg in (args.type, args.payment, args.interest,
                           args.principal, args.periods) if arg is not None]


def is_param_valid():
    if not interest:
        print('Incorrect parameters')
        return False

    if len(arg_lst) < 4:
        print('Incorrect parameters')
        return False

    if type not in TYPE_ALLOWED_VALUES:
        print('Incorrect parameters')
        return False

    if type == 'diff' and payment:
        print('Incorrect parameters')
        return False
    return True


def calculate_payment(m):
    nominal_interest = interest / 100 / 12

    form = (principal * (m - 1)) / periods
    final = principal - form
    diff_payment = principal / periods + nominal_interest * final

    return diff_payment


def calc_diff_payment():
    total_payment = 0
    for m in range(1, periods+1):
        diff_payment = math.ceil(calculate_payment(m))
        total_payment += diff_payment
        print(f'Month {m}: payment is {diff_payment}')
    return total_payment


def calc_overpay(total_payment):
    if type == 'diff':
        over_payment = total_payment - principal
    elif type == 'annuity' and payment and principal:
        over_payment = total_payment * 12 * payment - principal
    elif type == 'annuity' and principal:
        over_payment = total_payment * periods - principal
    elif type == 'annuity' and payment:
        over_payment = payment * periods - total_payment
    return over_payment


def calc_annuity_payment():
    nominal_interest = interest / 100 / 12
    form1 = nominal_interest * (1 + nominal_interest) ** periods
    form2 = (1 + nominal_interest) ** periods - 1
    total = math.ceil(principal * form1 / form2)

    print(f'Your annuity payment: {total}!')
    return total


def calculate_loan_principal():
    nominal_interest_rate = interest / 100 / 12
    form1 = nominal_interest_rate * \
        math.pow((1 + nominal_interest_rate), periods)
    form2 = math.pow((1 + nominal_interest_rate), periods) - 1
    princip = math.floor(payment / (form1 / form2))

    print(f'Your loan principal = {princip}!')
    return princip


def calculate_periods():
    nominal_interest_rate = interest / 100 / 12
    base = 1 + nominal_interest_rate
    x = payment / (payment - nominal_interest_rate * principal)

    number_of_months = math.ceil(math.log(x, base) + nominal_interest_rate * (x))

    years = number_of_months // 12
    print(f'It will take {years} years to repay this loan!')
    return years


def main():
    if type == 'diff':
        total_payment = calc_diff_payment()
    elif type == 'annuity' and principal and payment:
        total_payment = calculate_periods()
    elif type == 'annuity' and principal:
        total_payment = calc_annuity_payment()
    elif type == 'annuity' and payment:
        total_payment = calculate_loan_principal()

    over_payment = calc_overpay(total_payment)
    print(f'Overpayment = {over_payment}')


if is_param_valid():
    main()
