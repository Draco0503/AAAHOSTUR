class Offer:
    def __init__(self, id_offer = None, company_name = None, address = None, contact_name = None, contact_phone = None, contact_email = None, contact_name_2 = None, contact_phone_2 = None, contact_email_2 = None, verify = None, active = None, company = None, user_verify = None):
        self.id_offer = id_offer
        self.company_name = company_name
        self.address = address
        self.contact_name = contact_name
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.contact_name_2 = contact_name_2
        self.contact_phone_2 = contact_phone_2
        self.contact_email_2 = contact_email_2
        self.verify = verify
        self.active = active
        self.company = company
        self.user_verify = user_verify
    
    # Getters & Setters
    def get_id_offer(self):
        return self.id_offer
    
    def set_id_offer(self, new_value = None):
        self.id_account = new_value
    
    def get_account_holder(self):
        return self.account_holder
    
    def set_account_holder(self, new_value = None):
        self.account_holder = new_value

    def get_account_number(self):
        return self.account_number
    
    def set_account_number(self, new_value = None):
        self.account_number = new_value

    def get_sepa(self):
        return self.sepa
    
    def set_sepa(self, new_value = None):
        self.sepa = new_value

    def get_active(self):
        return self.active
    
    def set_active(self, new_value = None):
        self.active = new_value

    def get_company_holder(self):
        return self.company_holder
    
    def set_company_holder(self, new_value = None):
        self.company_holder = new_value

    # toJson
    def to_json(self):
        return {'id_account': self.id_account, 
                'account_holder': self.account_holder,
                'account_number': self.account_number,
                'sepa': self.sepa,
                'active': self.active,
                'company_holder': self.company_holder,
                } 