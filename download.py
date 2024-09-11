import pandas as pd


COLUMNS = ['title', 'price', 'rating', 'past_month_buyers', 'link']


def sort_by(items, attr, reverse=False):
	attr_list = [getattr(item, attr) for item in items]
	INF = float('-inf') if reverse else float('inf')
	attr_list = [x if x != 'N/A' else INF for x in attr_list]
	tuples = list(zip(attr_list, items))
	tuples.sort(reverse=reverse)
	return [y for _, y in tuples]


def to_csv(items, file_name='items.csv'):
	df = pd.DataFrame([item.to_list() for item in items], columns=COLUMNS)
	df.to_csv(file_name, index=False)


def to_txt(items, file_name='items.txt'):
	with open(file_name, 'w') as file:
		for item in items:
			file.write(item.to_str() + '\n')
