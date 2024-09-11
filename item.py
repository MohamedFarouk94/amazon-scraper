class Item:
	def __init__(self, item_dict):
		self.title = item_dict['title']
		self.price = item_dict['price']
		self.rating = item_dict['rating']
		self.past_month_buyers = item_dict['past_month_buyers']
		self.link = item_dict['link']

	def to_str(self, display_link=True):
		return f"""
Title: {self.title}
Price: {self.price}
Rating: {self.rating}
Past Month Buyers (>=): {self.past_month_buyers}""" + (f'\nLink: {self.link}' if display_link else '')

	def to_dict(self):
		return {
			'title': self.title,
			'price': self.price,
			'rating': self.rating,
			'past_month_buyers': self.past_month_buyers
		}

	def to_list(self):
		return [
			self.title,
			self.price,
			self.rating,
			self.past_month_buyers,
			self.link
		]

	def __eq__(self, other_item):
		return self.title == other_item.title and\
			self.price == other_item.price and\
			self.rating == other_item.rating and\
			self.past_month_buyers == other_item.past_month_buyers

	def __str__(self):
		s = self.title
		if len(s) < 35:
			return s
		else:
			return s[:32] + '...'

	def __hash__(self):
		return hash(f'{self.title} {self.price} {self.past_month_buyers} {self.rating}')

	__repr__ = __str__

	def __lt__(self, other_item):
		my_price = self.price if self.price != 'N/A' else float('inf')
		your_price = other_item.price if other_item.price != 'N/A' else float('-inf')
		return my_price < your_price
