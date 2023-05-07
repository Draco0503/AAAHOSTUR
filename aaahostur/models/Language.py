class Language:
    def __init__(self, id_language = None, name = None, lvl = None, certificate = None):
        self.id_language = id_language
        self.name = name
        self.lvl = lvl
        self.certificate = certificate
        
    # Getters & Setters
    def get_id_language(self):
        return self.id_language
    
    def set_id_language(self, new_value = None):
        self.id_language = new_value

    def get_name(self):
        return self.name
    
    def set_name(self, new_value = None):
        self.name = new_value

    def get_lvl(self):
        return self.lvl
    
    def set_lvl(self, new_value = None):
        self.lvl = new_value

    def get_certificate(self):
        return self.certificate
    
    def set_certificate(self, new_value = None):
        self.certificate = new_value

    # toJson
    def to_json(self):
        return {'id_language': self.id_language, 
                'name': self.name,
                'lvl': self.lvl,
                'certificate': self.certificate
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
