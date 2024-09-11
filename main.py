from amazonscrapper import get_amazon_search, start_driver, end_driver
from download import to_txt, to_csv, sort_by
from urllib.parse import quote


def main(item, n_pages,
	sorting=False, sorting_by='price', reverse=False,
	txt=False, csv=False, txt_file='items.txt', csv_file='items.csv', returning=True):

	item = quote(item)
	results = []
	start_driver()
	for i in range(n_pages):
		print(f'Getting Results from page {i + 1}...')
		url = f'https://www.amazon.com/s?k={item}&page={i + 1}'
		new_results = get_amazon_search(url)
		new_results = [x for x in new_results if x.title]
		new_results = list(set(new_results))
		results.extend(new_results)
		print(f'Till now found {len(results)} items.')
		print()
	end_driver()

	if sorting:
		results = sort_by(results, sorting_by, reverse=reverse)

	if txt:
		to_txt(results, file_name=txt_file)

	if csv:
		to_csv(results, file_name=csv_file)

	if returning:
		return results
