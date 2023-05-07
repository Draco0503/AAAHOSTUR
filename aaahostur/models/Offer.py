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
        self.id_offer = new_value
    
    def get_company_name(self):
        return self.company_name
    
    def set_company_name(self, new_value = None):
        self.company_name = new_value

    def get_address(self):
        return self.address
    
    def set_address(self, new_value = None):
        self.address = new_value

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

    def get_contact_name_2(self):
        return self.contact_name_2
    
    def set_contact_name_2(self, new_value = None):
        self.contact_name_2 = new_value

    def get_contact_phone_2(self):
        return self.contact_phone_2
    
    def set_contact_phone_2(self, new_value = None):
        self.contact_phone_2 = new_value

    def get_contact_email_2(self):
        return self.contact_email_2
    
    def set_contact_email_2(self, new_value = None):
        self.contact_email_2 = new_value 

    def get_verify(self):
        return self.verify
    
    def set_verify(self, new_value = None):
        self.verify = new_value

    def get_active(self):
        return self.active
    
    def set_active(self, new_value = None):
        self.active = new_value

    def get_company(self):
        return self.company
    
    def set_company(self, new_value = None):
        self.company = new_value

    def get_user_verify(self):
        return self.user_verify
    
    def set_user_verify(self, new_value = None):
        self.user_verify = new_value     

    # toJson
    def to_json(self):
        return {'id_offer': self.id_offer, 
                'company_name': self.company_name,
                'address': self.address,
                'contact_name': self.contact_name,
                'contact_phone': self.contact_phone,
                'contact_email': self.contact_email,
                'contact_name_2': self.contact_name_2,
                'contact_phone_2': self.contact_phone_2,
                'contact_email_2': self.contact_email_2,
                'verify': self.verify,
                'active': self.active,
                'company': self.company,
                'user_verify': self.user_verify
                }

#                                         %@@@@@@                             
#                                      @@@@@@@@@@@@*                          
#                              @@@@  @@@@@@@@@@@@@@#                          
#                                 &@@@@#%@@@@@@@@@@#                          
#                     ,@.,,,,,,,,,,,,,@@@@@@@##@@@@                           
#                 @.,,,,,,,,,,,,,,,,,,,,,,,.@@@@@@@                           
#             @,,,,,,,,,,,,,,,,,,@,,,,,,(*,,,,,,,@@@@@&                       
#           @,,,,,,,,,,,,,,,,,,,%,,,,,,,,,,,,,,,,,,@ .@@@                     
#         @,,,,,,,,,,,,,,,,,,,,,,,@@@@@@@,,,,,,,,,,,,@                        
#       &,,,,,,@,,,,,,,,,,,,,,,,@@@@@@@@@@@@@,,,,,,,,,,@                      
#      *,,,,,,,,,,,,,,,,,,,,,,,,@@@@@@@@  @@@@@,,,,,,,,,/                     
#     %,@@/,,,,,,,,,,,,,,,,,,,,,@@@@@@@@@@@@@@@,,,,,,,,,,,.                   
#    @,,,,,,,,@,,,,,,,,,,,,,,,,,#@@@@@@@@@@@@@@,,,,,,,,,,,,,                  
#    @,,,,,,,,,,,,,,,,,,,,,,,,,,,,%@@@@@@@@@@@@,,,,,,,,,,,,,*                 
#    ,,,,,,,,,,,,,,,,,,,,@,,,,,,,,,,,,*@@@@,,,,,,,@,,,,@,,,,,/                
#   &,@@@(.@*,,,,,,,,,,,,,&,,,,,,,,,,,,,,,,,,,,,,,@%,,,,%,,,,,*               
#   @,,,,,,,,,,,,,,,,,,,,,@,,,,,,,,,,,,,,,,,,,%(#######@,,,,,,,&              
#   &,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,@################,,,,,,,&             
#    ,,,,,,,,@,,,,,,,,,,,,,,,,,,,,/%#####################%,,,,,,,#            
#    &,,,,,,,,,,,,,,,,,,,#,,,,,*#############*@@@,#######@,,,,,,,,            
#    @,,,,,,,,,,,,,,,,,,,@,,,,,%@@/,,,,,%@,,,,,,,,,,,,,@#@,,,,,,,,@           
#    .,/,,,,,,,,,,,,,,,,*@,,,,,,,@,,,,,,,,,,,@,,,,,,,,,,*,,,,,,,,,,@          
#    ,,,##@#.,/&,,,,,,,#@,,,,,,,,,,/&,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.          
#    ,,,,,,#,,,,,,,,,,&,,,,,,,,,,,,,,,,@@/,,,,,,,,,,#@,,,,,,,,,,,,,,@         
#    ,,,,,,,,,%@@@@@.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.        
#   &,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,@@*,,,,,*@,,,/,,,,,,,,,,,,,,,#       
#   @,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,@,,,,,,,,,,,,*%,,,,,,,,,,,,,,,@@       
#  ,@@@@@@@%@(,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,@@@@%      
#  @@@@@@@@@@@@@@@@&((@@%/,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,@@@@@@@@@     
#  @@@@@@@@@@@@@@@(((((@   @#####@     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    
# #@@@@@@@@@@@@@@(((((((@     @@    &(((((@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   
# @@@@@@@@@@@@@@@@@@@@@@@    ##@    @@@(((@@@@@@@@@@@@@@@@@@@@@@@@@@@%%#      
#    @%@&@@@@@@@@@@@@@@@    /####   &@@@@@@@@@@@@@@@@@@@@@@@@#/               
#              *@@@@@@@    @######@  @@@@@@@@%@@@@@@(***, 