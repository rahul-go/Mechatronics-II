


class Controller:
    
    
    def __init__(self, K_P, x_set):
        print('Creating a controller!')
        self.K_P = K_P
        self.x_set = x_set
    def run(self, x_act):     

        level = self.K_P*(self.x_set-x_act)
        if level > 100:
            level = 100
        elif level < -100: 
            level = -100
        return level
    def set_K_P(self, K_P):
        self.K_P = K_P
    def set_x_set(self, x_set):
        self.x_set = x_set
            
    
            
    
    
   
    
    
    