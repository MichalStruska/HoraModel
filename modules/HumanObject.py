import numpy as np

class Human:
    def __init__(self, anthropometry, environment):
        self.anthropometry = anthropometry
	self.surface_area = GetSurfaceArea()
	self.initial_mass = anthropometry("initial_mass")
	self.stature = anthropometry("stature")
	self.mechanical_efficiency = 0.2
	self.air_temperature = environment.air_temperature

    def GetSurfaceArea(self):
	return 0.20247 * (self.initial_mass**0.425) * (self.stature**0.725)
    
    

    class RespiratorySystem(self, human, environment):
	def __init__(self):
	    self.metabolic_heat = human.metabolic_heat
	    

	def GetRespiratoryHeatLoss(self):
	    self.expired_temperature = self.GetExpiredTemperature()
	    return GetRespiratoryConvection() + GetRespiratoryEvaporation()

	def GetExpiredTemperature(self):
	    return 32.6 + 0.066*environment.air_temperature + 32*0.622*environment.air_pressure/(environment.air_pressure390 - environment.air_pressure)
	

	def GetRespiratoryConvection(self):
	    return 0.0014 * (human.metabolic_heat/(1-mechanical_efficiency)) * (air_temperature-expired_temperature)

	def GetRespiratoryEvaporation():
	    return 0.0173*(human.metabolic_heat/(1-human.mechanical_efficiency))*(5.87-environment.air_pressure)

    class Skin:
        def __init__(self, area):
            self.area = area

	def 

    class Core:
	def __init__(self, anthropometry):

