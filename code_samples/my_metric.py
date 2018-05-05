from checks import AgentCheck
from random import randint

class MyMetricCheck(AgentCheck):
	def check(self, instance):
		floor = instance['floor']
		ceiling = instance['ceiling']
		self.gauge('my_metric', randint(floor, ceiling))