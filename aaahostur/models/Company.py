class Company:
    def __init__(self, id_company = None, range = None, cif = None, address = None, cp = None, city = None, province = None, contact_name = None, contact_phone = None, contact_email = None, description = None, verify = None, active = None, company_parent = None, user_verify = None):
        self.id_company = id_company
        self.range = range
        self.cif = cif
        self.address = address
        self.cp = cp
        self.city = city
        self.province = province
        self.contact_name = contact_name
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.description = description
        self.verify = verify
        self.active = active
        self.company_parent = company_parent
        self.user_verify = user_verify
    
    # Getters & Setters
    def get_id_company(self):
        return self.id_company
    
    def set_id_company(self, new_value = None):
        self.id_company = new_value
    
    def get_range(self):
        return self.range
    
    def set_range(self, new_value = None):
        self.range = new_value

    def get_cif(self):
        return self.cif
    
    def set_cif(self, new_value = None):
        self.cif = new_value

    def get_address(self):
        return self.address
    
    def set_address(self, new_value = None):
        self.address = new_value

    def get_cp(self):
        return self.cp
    
    def set_cp(self, new_value = None):
        self.cp = new_value

    def get_city(self):
        return self.city
    
    def set_city(self, new_value = None):
        self.city = new_value

    def get_province(self):
        return self.province
    
    def set_province(self, new_value = None):
        self.province = new_value

    def get_contact_name(self):
        return self.contact_name
    
    def set_contact_name(self, new_value = None):
        self.contact_name = new_value

    def get_contact_phone(self):
        return self.contact_phone
    
    def set_contact_phone(self, new_value = None):
        self.contact_phone = new_value

    def get_contact_email(self):
        return self.contact_email
    
    def set_contact_email(self, new_value = None):
        self.contact_email = new_value

    def get_description(self):
        return self.description
    
    def set_description(self, new_value = None):
        self.description = new_value

    def get_verify(self):
        return self.verify
    
    def set_verify(self, new_value = None):
        self.verify = new_value

    def get_active(self):
        return self.active
    
    def set_active(self, new_value = None):
        self.active = new_value

    def get_company_parent(self):
        return self.company_parent
    
    def set_company_parent(self, new_value = None):
        self.company_parent = new_value

    def get_user_verify(self):
        return self.user_verify
    
    def set_user_verify(self, new_value = None):
        self.user_verify = new_value

    # toJson
    def to_json(self):
        return {'id_company': self.id_company, 
                'range': self.range,
                'cif': self.cif,
                'address': self.address,
                'cp': self.cp,
                'city': self.city,
                'province': self.province,
                'contact_name': self.contact_name,
                'contact_phone': self.contact_phone,
                'contact_email': self.contact_email,
                'description': self.description,
                'verify': self.verify,
                'active': self.active,
                'company_parent': self.company_parent,
                'user_verify': self.user_verify
                }