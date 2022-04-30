class Password:
    def __init__(self, password):
        self.password = password

    def validate(self):        
        vals = {
        'Password must contain an uppercase letter.': lambda s: any(x.isupper() for x in s),
        'Password must contain a lowercase letter.': lambda s: any(x.islower() for x in s),
        'Password must contain a digit.': lambda s: any(x.isdigit() for x in s),
        'Password must be at least 8 characters.': lambda s: len(s) >= 8,
        'Password cannot contain white spaces.': lambda s: not any(x.isspace() for x in s)            
        } 
        valid = True  
        for n, val in vals.items():                         
           if not val(self.password):                   
               valid = False
               return n
        return valid                

    def compare(self, password2):
        if self.password == password2:
            return True


if __name__ == '__main__':
    input_password = input('Insert Password: ')
    input_password2 = input('Repeat Password: ')
    p = Password(input_password)
    if p.validate() is True:
        if p.compare(input_password2) is True:
            print('OK')
    else:
       print(p.validate())
