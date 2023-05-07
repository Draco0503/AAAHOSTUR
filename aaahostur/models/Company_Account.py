class Company_Account:
    def __init__(self, id_account = None, account_holder = None, account_number = None, sepa = None, active = None, company_holder = None):
        self.id_account = id_account
        self.account_holder = account_holder
        self.account_number = account_number
        self.sepa = sepa
        self.active = active
        self.company_holder = company_holder
    
    # Getters & Setters
    def get_id_account(self):
        return self.id_account
    
    def set_id_account(self, new_value = None):
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