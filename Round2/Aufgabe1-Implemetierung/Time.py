class Time:
	def __init__(self, hour, minute, second):
		self.hour = hour
		self.minute = minute
		self.second = second

	# Vergleichsmethode
	def __lt__(self, other):
		if self.hour < other.hour:
			return True
		else:
			if self.hour == other.hour:
				if self.minute < other.minute:
					return True
				else:
					if self.minute == other.minute:
						if self.second < other.second:
							return True
		return False

	def __str__(self):
		return "{}:{}:{}".format(self.hour, self.minute, self.second)

	def __repr__(self):
		return "{}:{}:{}".format(self.hour, self.minute, self.second)

	def seconds_from_midnight(self):
		return min_in_sec(self.hour * 60) + min_in_sec(self.minute) + self.second


# Addition von Sekunden auf eine Uhrzeit (Übergang auf anderen Tag nicht möglich)
def add_seconds(t, s):
	new_time = Time(t.hour, t.minute, t.second)
	if s < 60:
		sec = t.second + s
	else:
		if s < 3600:
			mod = s % 60
			sec = t.second + mod
			minu = t.minute + (s - mod)/60
		else:
			mod1 = s % 3600
			mod2 = mod1 % 60
			sec = t.second + mod2
			minu = t.minute + (mod1 - mod2)/60
			new_time.hour = t.hour + (s - mod1)/3600
		if minu < 60:
			new_time.minute = minu
		else:
			new_time.hour += 1
			new_time.minute = minu - 60
	if sec < 60:
		new_time.second = sec
	else:
		new_time.minute += 1
		new_time.second = sec - 60
	new_time.hour = int(new_time.hour)
	new_time.minute = int(new_time.minute)
	new_time.second = int(new_time.second)
	return new_time


# Subtraktion von Sekunden von einer Uhrzeit (Übergang auf anderen Tag nicht möglich)
def subtract_seconds(t, s):
	new_time = Time(t.hour, t.minute, t.second)
	if s < 60:
		sec = t.second - s
	else:
		if s < 3600:
			mod = s % 60
			sec = t.second - mod
			minu = t.minute - (s - mod)/60
		else:
			mod1 = s % 3600
			mod2 = mod1 % 60
			sec = t.second - mod2
			minu = t.minute - (mod1 - mod2)/60
			new_time.hour = t.hour - (s - mod1)/3600
		if minu >= 0:
			new_time.minute = minu
		else:
			new_time.hour -= 1
			new_time.minute = 60 + minu
	if sec >= 0:
		new_time.second = sec
	else:
		new_time.minute -= 1
		new_time.second = 60 + sec
	new_time.hour = int(new_time.hour)
	new_time.minute = int(new_time.minute)
	new_time.second = int(new_time.second)
	return new_time


# Hilfsmethode
def min_in_sec(mins):
	return mins * 60


# Hilfsmethode
def sec_in_min(secs):
	return secs / 60








