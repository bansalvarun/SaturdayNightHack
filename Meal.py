class Meal():
	def __init__(self, typ, day, what):
		self.day = day
		self.type = typ
		self.what = what
	def getMealId(self):
		return "%s.%s" % (self.day, self.type)