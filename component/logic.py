# Logic and Constant
BLANK = " "

def swife_element(data:list, with_:int="", whome:(int, str)=BLANK) -> list:
	new_puzzle_data = []
	with_data = data[get_index(data=data, num=with_)]
	whome_data = data[get_index(data=data)]

	for i in range(len(data)):
		if data[i]["num"] == with_:
			new_puzzle_data.append(whome_data)
		elif data[i]["num"] == whome:
			new_puzzle_data.append(with_data)
		else:
			new_puzzle_data.append(data[i])

	return new_puzzle_data

def get_index(data:list, num:(int, str)=BLANK) -> int:
	"""Return index number of "num(param)" from the "data(param)" """
	for i in range(len(data)):
		if data[i]["num"] == num:
			return i

def get_num(data:list, num):
	"""Internal use it only target the num key of data(param) 
		and return value
	"""
	return data[num]["num"]
