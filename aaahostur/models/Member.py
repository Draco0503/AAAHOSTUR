class Member:
    def __init__(self, id_member = None, name = None, surname = None, dni = None, address = None, cp = None, city = None, province = None, pna_address = None, pna_cp = None, pna_city = None, pna_province = None, gender = None, land_line = None, mobile = None, profile_picture = None, birth_date = None, join_date = None, cancelation_date = None, active = None, verify = None, user_verify = None):
        self.id_member = id_member
        self.name = name
        self.surname = surname
        self.dni = dni
        self.address = address
        self.cp = cp
        self.city = city
        self.province = province
        self.pna_address = pna_address
        self.pna_cp = pna_cp
        self.pna_city = pna_city
        self.pna_province = pna_province
        self.gender = gender
        self.land_line = land_line
        self.mobile = mobile
        self.profile_picture = profile_picture
        self.birth_date = birth_date
        self.join_date = join_date
        self.cancelation_date = cancelation_date
        self.active = active
        self.verify = verify
        self.user_verify = user_verify
    
    # Getters & Setters
    def get_id_member(self):
        return self.id_member
    
    def set_id_member(self, new_value = None):
        self.id_member = new_value
    
    def get_name(self):
        return self.name
    
    def set_name(self, new_value = None):
        self.name = new_value

    def get_surname(self):
        return self.surname
    
    def set_surname(self, new_value = None):
        self.surname = new_value

    def get_dni(self):
        return self.dni
    
    def set_dni(self, new_value = None):
        self.dni = new_value

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

    def get_pna_address(self):
        return self.pna_address
    
    def set_pna_address(self, new_value = None):
        self.pna_address = new_value

    def get_pna_cp(self):
        return self.pna_cp
    
    def set_pna_cp(self, new_value = None):
        self.pna_cp = new_value

    def get_pna_city(self):
        return self.pna_city
    
    def set_pna_city(self, new_value = None):
        self.pna_city = new_value

    def get_pna_province(self):
        return self.pna_province
    
    def set_pna_province(self, new_value = None):
        self.pna_province = new_value

    def get_gender(self):
        return self.gender
    
    def set_gender(self, new_value = None):
        self.gender = new_value

    def get_land_line(self):
        return self.land_line
    
    def set_land_line(self, new_value = None):
        self.land_line = new_value

    def get_mobile(self):
        return self.mobile
    
    def set_mobile(self, new_value = None):
        self.mobile = new_value

    def get_profile_picture(self):
        return self.profile_picture
    
    def set_profile_picture(self, new_value = None):
        self.profile_picture = new_value

    def get_birth_date(self):
        return self.birth_date
    
    def set_birth_date(self, new_value = None):
        self.birth_date = new_value

    def get_join_date(self):
        return self.join_date
    
    def set_join_date(self, new_value = None):
        self.join_date = new_value

    def get_cancelation_date(self):
        return self.cancelation_date
    
    def set_cancelation_date(self, new_value = None):
        self.cancelation_date = new_value

    def get_active(self):
        return self.active
    
    def set_active(self, new_value = None):
        self.active = new_value

    def get_verify(self):
        return self.verify
    
    def set_verify(self, new_value = None):
        self.verify = new_value

    def get_user_verify(self):
        return self.user_verify
    
    def set_user_verify(self, new_value = None):
        self.user_verify = new_value

    # toJson
    def to_json(self):
        return {'id_member': self.id_member,
                'name': self.name,
                'surname': self.surname,
                'dni': self.dni,
                'address': self.address,
                'cp': self.cp,
                'city': self.city,
                'province': self.province,
                'pna_address': self.pna_address,
                'pna_cp': self.pna_cp,
                'pna_city': self.pna_city,
                'pna_province': self.pna_province,
                'gender': self.gender,
                'land_line': self.land_line,
                'mobile': self.mobile,
                'profile_picture': self.profile_picture,
                'birth_date': self.birth_date,
                'join_date': self.join_date,
                'cancelation_date': self.cancelation_date,
                'active': self.active,
                'verify': self.verify,
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