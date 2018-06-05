

def parse_number(query):
	zh_numbers = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六':6, '七':7, '八':8, '九':9, '十': 10, 
				'十一': 11, '十二': 12,'十三': 13,'十四': 14,'十五': 15,'十六': 16,'十七': 17,'十八': 11,'十九': 11}
	result = -1
	for zh_number in zh_numbers.keys():
		if query.startswith(zh_number):
			result = zh_numbers[zh_number]
	if result < 1:
		try:
			result = int(query)
		except:
			result = 0
	return result
