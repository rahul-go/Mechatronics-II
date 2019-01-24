


class Controller:
    
    
    def __init__(self, K_P, x_set, motor, encoder):
        print('Creating a controller!')
        self.motor = motor
        self.encoder = encoder
        self.K_P = K_P
        self.x_set = x_set
    def run(self):     
        self.x_act = self.encoder.read()
        level = self.K_P*(self.x_act-self.x_set)
        self.motor.set_duty_cycle(level)
    
            
    
    
   
    
    
    