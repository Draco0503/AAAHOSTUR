
class Review:
    def __init__(self, id_review = None, score = None, description = None, business_sender = None, verify = None, active = None, user_verify = None, company = None, member = None):
        self.id_review = id_review
        self.score = score
        self.description = description
        self.business_sender = business_sender
        self.verify = verify
        self.active = active
        self.user_verify = user_verify
        self.company = company
        self.member = member
    
    # Getters & Setters
    def get_id_review(self):
        return self.id_review
    
    def set_id_review(self, new_value = None):
        self.id_review = new_value
    
    def get_score(self):
        return self.score
    
    def set_score(self, new_value = None):
        self.score = new_value

    def get_description(self):
        return self.description
    
    def set_description(self, new_value = None):
        self.description = new_value

    def get_business_sender(self):
        return self.business_sender
    
    def set_business_sender(self, new_value = None):
        self.business_sender = new_value

    def get_verify(self):
        return self.verify
    
    def set_verify(self, new_value = None):
        self.verify = new_value

    def get_active(self):
        return self.active
    
    def set_active(self, new_value = None):
        self.active = new_value

    def get_user_verify(self):
        return self.user_verify
    
    def set_user_verify(self, new_value = None):
        self.user_verify = new_value    

    def get_company(self):
        return self.company
    
    def set_company(self, new_value = None):
        self.company = new_value 

    def get_member(self):
        return self.member
    
    def set_member(self, new_value = None):
        self.member = new_value 

    # toJson
    def to_json(self):
        return {'id_review': self.id_review, 
                'score': self.score,
                'description': self.description,
                'business_sender': self.business_sender,
                'verify': self.verify,
                'active': self.active,
                'user_verify': self.user_verify,
                'company': self.company,
                'member': self.member
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