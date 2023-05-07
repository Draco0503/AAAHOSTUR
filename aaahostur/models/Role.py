class Role:
    def __init__(self, id_role = None, name = None, description = None, canVerifyMember = None, canVerifyCompany = None, canVerifyAdmin = None, canVerifyOffer = None, canVerifyReview = None, canSeeOffer = None, canApplyOffer = None, canMakeOffer = None, canSeeSection = None, canMakeSection = None, canActiveMember = None, canActiveCompany = None, canActiveSection = None, canActiveOffer = None, canActiveReview = None, canActiveCompanyBankAcc = None, canActiveMemberBankAcc = None, canSeeReview = None, canMakeReview = None):
        self.id_role = id_role
        self.name = name
        self.description = description
        self.canVerifyMember = canVerifyMember
        self.canVerifyCompany = canVerifyCompany
        self.canVerifyAdmin = canVerifyAdmin
        self.canVerifyOffer = canVerifyOffer
        self.canVerifyReview = canVerifyReview
        self.canSeeOffer = canSeeOffer
        self.canApplyOffer = canApplyOffer
        self.canMakeOffer = canMakeOffer
        self.canSeeSection = canSeeSection
        self.canMakeSection = canMakeSection
        self.canActiveMember = canActiveMember
        self.canActiveCompany = canActiveCompany
        self.canActiveSection = canActiveSection
        self.canActiveOffer = canActiveOffer
        self.canActiveReview = canActiveReview
        self.canActiveCompanyBankAcc = canActiveCompanyBankAcc
        self.canActiveMemberBankAcc = canActiveMemberBankAcc
        self.canSeeReview = canSeeReview
        self.canMakeReview = canMakeReview

    # Getters & Setters
    def get_id_role(self):
        return self.id_role
    
    def set_id_role(self, new_value = None):
        self.id_role = new_value
    
    def get_name(self):
        return self.name
    
    def set_name(self, new_value = None):
        self.name = new_value

    def get_description(self):
        return self.description
    
    def set_description(self, new_value = None):
        self.description = new_value

    def get_canVerifyMember(self):
        return self.canVerifyMember
    
    def set_canVerifyMember(self, new_value = None):
        self.canVerifyMember = new_value

    def get_canVerifyCompany(self):
        return self.canVerifyCompany
    
    def set_canVerifyCompany(self, new_value = None):
        self.canVerifyCompany = new_value

    def get_canVerifyAdmin(self):
        return self.canVerifyAdmin
    
    def set_canVerifyAdmin(self, new_value = None):
        self.canVerifyAdmin = new_value

    def get_canVerifyOffer(self):
        return self.canVerifyOffer
    
    def set_canVerifyOffer(self, new_value = None):
        self.canVerifyOffer = new_value

    def get_canVerifyReview(self):
        return self.canVerifyReview
    
    def set_canVerifyReview(self, new_value = None):
        self.canVerifyReview = new_value

    def get_canSeeOffer(self):
        return self.canSeeOffer
    
    def set_canSeeOffer(self, new_value = None):
        self.canSeeOffer = new_value

    def get_canApplyOffer(self):
        return self.canApplyOffer
    
    def set_canApplyOffer(self, new_value = None):
        self.canApplyOffer = new_value

    def get_canMakeOffer(self):
        return self.canMakeOffer
    
    def set_canMakeOffer(self, new_value = None):
        self.canMakeOffer = new_value

    def get_canSeeSection(self):
        return self.canSeeSection
    
    def set_canSeeSection(self, new_value = None):
        self.canSeeSection = new_value

    def get_canMakeSection(self):
        return self.canMakeSection
    
    def set_canMakeSection(self, new_value = None):
        self.canMakeSection = new_value

    def get_canActiveMember(self):
        return self.canActiveMember
    
    def set_canActiveMember(self, new_value = None):
        self.canActiveMember = new_value

    def get_canActiveCompany(self):
        return self.canActiveCompany
    
    def set_canActiveCompany(self, new_value = None):
        self.canActiveCompany = new_value

    def get_canActiveSection(self):
        return self.canActiveSection
    
    def set_canActiveSection(self, new_value = None):
        self.canActiveSection = new_value

    def get_canActiveOffer(self):
        return self.canActiveOffer
    
    def set_canActiveOffer(self, new_value = None):
        self.canActiveOffer = new_value

    def get_canActiveReview(self):
        return self.canActiveReview
    
    def set_canActiveReview(self, new_value = None):
        self.canActiveReview = new_value

    def get_canActiveCompany(self):
        return self.canActiveCompany
    
    def set_canActiveCompany(self, new_value = None):
        self.canActiveCompany = new_value

    def get_canActiveSection(self):
        return self.canActiveSection
    
    def set_canActiveSection(self, new_value = None):
        self.canActiveSection = new_value

    def get_canActiveOffer(self):
        return self.canActiveOffer
    
    def set_canActiveOffer(self, new_value = None):
        self.canActiveOffer = new_value

    def get_canActiveReview(self):
        return self.canActiveReview
    
    def set_canActiveReview(self, new_value = None):
        self.canActiveReview = new_value

    def get_canActiveCompanyBankAcc(self):
        return self.canActiveCompanyBankAcc
    
    def set_canActiveCompanyBankAcc(self, new_value = None):
        self.canActiveCompanyBankAcc = new_value

    def get_canActiveMemberBankAcc(self):
        return self.canActiveMemberBankAcc
    
    def set_canActiveMemberBankAcc(self, new_value = None):
        self.canActiveMemberBankAcc = new_value

    def get_canSeeReview(self):
        return self.canSeeReview
    
    def set_canSeeReview(self, new_value = None):
        self.canSeeReview = new_value

    def get_canMakeReview(self):
        return self.canMakeReview
    
    def set_canMakeReview(self, new_value = None):
        self.canMakeReview = new_value

    # toJson
    def to_json(self):
        return {'id_role': self.id_role, 
                'name': self.name,
                'description': self.description,
                'canVerifyMember': self.canVerifyMember,
                'canVerifyCompany': self.canVerifyCompany,
                'canVerifyAdmin': self.canVerifyAdmin,
                'canVerifyOffer': self.canVerifyOffer,
                'canVerifyReview': self.canVerifyReview,
                'canSeeOffer': self.canSeeOffer,
                'canApplyOffer': self.canApplyOffer,
                'canMakeOffer': self.canMakeOffer,
                'canSeeSection': self.canSeeSection,
                'canMakeSection': self.canMakeSection,
                'canActiveMember': self.canActiveMember,
                'canActiveCompany': self.canActiveCompany,
                'canActiveSection': self.canActiveSection,
                'canActiveOffer': self.canActiveOffer,
                'canActiveReview': self.canActiveReview,
                'canActiveCompanyBankAcc': self.canActiveCompanyBankAcc,
                'canActiveMemberBankAcc': self.canActiveMemberBankAcc,
                'canSeeReview': self.canSeeReview,
                'canMakeReview': self.canMakeReview
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