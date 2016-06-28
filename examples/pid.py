class PID:
	def __init__(self, Epsilon=.01, Kp=1, Ki=1, Kd=1, Imax=300, Imin=-300):
		self.Ep = Epsilon
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd

		self.Imax = Imax
		self.Imin = Imin
		self.lastError = 0
		self.cumulativeError = 0

	def updateCumulativeError(self, error):
		self.cumulativeError += error
		if self.cumulativeError > self.Imax:
			self.cumulativeError = self.Imax
		elif self.cumulativeError < self.Imin:
			self.cumulativeError = self.Imin

	def proccess(self, error, derivative=None, integral=None):
		if -self.Ep < error < self.Ep:
			return 0, 0, 0

		P = self.Kp * error
		self.updateCumulativeError(error)
		if integral != None:
			I = self.Ki * integral
		else:
			I = self.Ki * self.cumulativeError

		if derivative != None:
			D = self.Kd * derivative
		else:
			D = self.Kd * (error - self.lastError)
		self.lastError = error

		return P, I, D