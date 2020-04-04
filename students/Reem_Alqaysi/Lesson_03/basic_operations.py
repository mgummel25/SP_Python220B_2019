"""Basic operations for the customer_model"""

import logging
import peewee as pw
from customer_model import Customer, DATABASE

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


DATABASE.drop_tables([Customer])
DATABASE.create_tables([Customer])
""""
#for testing
name = 'Reem'
lastname = 'alqaysi'
home_address = '123 45th st bothell wa 98011'
phone_number =1234567890
email_address = 'abc123@uw.edu'
status = 1
credit_limit =222
"""

def add_customer(name, lastname, home_address, phone_number, email_address,
                 status, credit_limit):
    """create a new customer object in the database table"""
    try:
        with DATABASE.transaction():
            new_customer = Customer.create(
                name=name,
                lastname=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                status=status,
                credit_limit=credit_limit)
            new_customer.save()
            LOGGER.info("adding Customer: %s is successful", name)
            return new_customer
    except pw.IntegrityError as exc:
        LOGGER.info("Error creating %s; Exception: %s", name, exc)


def search_customer(customer_id):
    """search for an exisitng customer object in the database table"""
    try:
        a_customer = Customer.get(Customer.customer_id == customer_id)
        a_customer_info = {'name': a_customer.name,
                           'lastname': a_customer.lastname,
                           'phone_number': a_customer.phone_number,
                           'email_address': a_customer.email_address}
        LOGGER.info(a_customer_info)
        return a_customer_info
    except pw.DoesNotExist:
        a_customer_info = {}
        LOGGER.info(a_customer_info)
        return a_customer_info


def delete_customer(customer_id):
    """delete an exiting customer object from the database table"""
    try:
        a_customer = Customer.get(Customer.customer_id == customer_id)
        a_customer.delete_instance()
        LOGGER.info('Database delete successful')
    except pw.DoesNotExist:
        LOGGER.info('Customer ID provided does not exist')


def update_customer_credit(customer_id, credit_limit):
    """update the credit limit for an existing customer"""
    try:
        a_customer = Customer.get(Customer.customer_id == customer_id)
        a_customer.credit_limit = credit_limit
        a_customer.save()
        LOGGER.info('Database update successful')
    except pw.DoesNotExist:
        LOGGER.info('Customer ID provided does not exist')


def list_active_customers():
    """list all active customer: status = 1 (Active), status = 0 (Inactive)"""
    active_count = 0
    for _ in Customer.select().where(Customer.status == True):
        active_count += 1

    LOGGER.info("Total active customers: %d", active_count)
    return active_count
""""
#for Testing
if __name__ == '__main__':
    add_customer(name, lastname, home_address, phone_number, email_address,
                 status, credit_limit)
    list_active_customers()
"""
