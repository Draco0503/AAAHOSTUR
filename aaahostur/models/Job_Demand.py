class Job_Demand:   
    def __init__(self, id_job_demand = None, vacancies = None, monthly_salary = None, contract_type = None, schedule = None, working_day = None, shift = None, holidays = None, experience = None, vehicle = None, geographical_mobility = None, disability = None, disability_grade = None, others = None, offer = None):
        self.id_job_demand = id_job_demand
        self.vacancies = vacancies
        self.monthly_salary = monthly_salary
        self.contract_type = contract_type
        self.schedule = schedule
        self.working_day = working_day
        self.shift = shift
        self.holidays = holidays
        self.experience = experience
        self.vehicle = vehicle
        self.geographical_mobility = geographical_mobility
        self.disability = disability
        self.disability_grade = disability_grade
        self.others = others
        self.offer = offer
    
    # Getters & Setters
    def get_id_job_demand(self):
        return self.id_job_demand
    
    def set_id_job_demand(self, new_value = None):
        self.id_job_demand = new_value
    
    def get_vacancies(self):
        return self.vacancies
    
    def set_vacancies(self, new_value = None):
        self.vacancies = new_value

    def get_monthly_salary(self):
        return self.monthly_salary
    
    def set_monthly_salary(self, new_value = None):
        self.monthly_salary = new_value

    def get_contract_type(self):
        return self.contract_type
    
    def set_contract_type(self, new_value = None):
        self.contract_type = new_value

    def get_schedule(self):
        return self.schedule
    
    def set_schedule(self, new_value = None):
        self.schedule = new_value

    def get_working_day(self):
        return self.working_day
    
    def set_working_day(self, new_value = None):
        self.working_day = new_value

    def get_shift(self):
        return self.shift
    
    def set_shift(self, new_value = None):
        self.shift = new_value    

    def get_holidays(self):
        return self.holidays
    
    def set_holidays(self, new_value = None):
        self.holidays = new_value 

    def get_experience(self):
        return self.experience
    
    def set_experience(self, new_value = None):
        self.experience = new_value

    def get_vehicle(self):
        return self.vehicle
    
    def set_vehicle(self, new_value = None):
        self.vehicle = new_value 

    def get_geographical_mobility(self):
        return self.geographical_mobility
    
    def set_geographical_mobility(self, new_value = None):
        self.geographical_mobility = new_value 

    def get_disability(self):
        return self.disability
    
    def set_disability(self, new_value = None):
        self.disability = new_value 

    def get_disability_grade(self):
        return self.disability_grade
    
    def set_disability_grade(self, new_value = None):
        self.disability_grade = new_value 

    def get_others(self):
        return self.others
    
    def set_others(self, new_value = None):
        self.others = new_value 

    def get_offer(self):
        return self.offer
    
    def set_offer(self, new_value = None):
        self.offer = new_value 

    # toJson
    def to_json(self):
        return {'id_job_demand': self.id_job_demand, 
                'vacancies': self.vacancies,
                'monthly_salary': self.monthly_salary,
                'contract_type': self.contract_type,
                'schedule': self.schedule,
                'working_day': self.working_day,
                'shift': self.shift,
                'holidays': self.holidays,
                'experience': self.experience,
                'vehicle': self.vehicle,
                'geographical_mobility': self.geographical_mobility,
                'disability': self.disability,
                'disability_grade': self.disability_grade,
                'others': self.others,
                'offer': self.offer
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