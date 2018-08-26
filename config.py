class Develop:
    DEBUG = True

class Testing:
    DEBUG = True
    
class Production:
    DEBUG = False
    
app_config = {
    "develop": Develop,
    "testing" : Testing,
    "production": Production
    
 }