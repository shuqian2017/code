# -*-coding:utf-8 -*-

from conf import  settings
from core import accounts
from core import logger

def make_transaction(log_obj, account_data, tran_type, amount, **kwars):
    '''
    deal all the user transactions
    :param account_data:    user accounts data
    :param tran_type:   transaction type
    :param amount:  transaction amount
    :param kwars:   mainly for logging usage
    :return:
    '''
    amount = float(amount)
    if tran_type in settings.TRANSACTION_TYPE:

        interest = amount * settings.TRANSACTION_TYPE[tran_type]['interest']
        old_balance = account_data['balance']
        if settings.TRANSACTION_TYPE[tran_type]['action'] == 'plus':
            new_balance = old_balance + amount + interest
        elif settings.TRANSACTION_TYPE[tran_type]['action'] == 'minus':
            new_balance = old_balance - amount - interest

            if new_balance < 0:
                print('''\033[31;1mYour credit [%s] is not enough for this transaction [-%s], your current balance is [%s]\
                ''' % (account_data['credit'], (amount + interest), old_balance))
                return

        account_data['balance'] = new_balance
        accounts.dump_account(account_data)    # save the new balance back to file
        log_obj.info('accounts: %s   action: %s  amount: %s  interest:%s' % (account_data['id'], tran_type, amount, interest))
        return account_data

    else:
        print("\033[31;1mTransaction type [%s] is not exist!\033[0m" % tran_type)
