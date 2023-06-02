# auxiliar functions

# check NIF/NIE/DNI
def validate_nif(nif= ''):
    # NIF --> fiscal identification number (company/member)
    # NIE --> foreign identification number (member)
    # DNI --> national identification number (member)
    # CIF --> doesnt exists anymore, now is NIF
    all_control_digits= 'TRWAGMYFPDXBNJZSQVHLCKE'
    foreign_digits= 'XYZ'
    numbers= '1234567890'
    foreign_replace= {'X':'0', 
                      'Y':'1', 
                      'Z':'2'}
    validation= False
    nif= nif.upper() # lower leters problem solved

    if len(nif) == 9:
        control_digit= nif[8]
        remaining_document= nif[:8]

        if remaining_document[0] in foreign_digits:
            remaining_document= remaining_document.replace(remaining_document[0], 
                                                           foreign_replace[remaining_document[0]])
            
        if (len(remaining_document) == len([num for num in remaining_document if num in numbers])) and (all_control_digits[int(remaining_document) % 23] == control_digit):
            validation= True
        else:
            validation= False

    else:
        validation= False

    return validation
