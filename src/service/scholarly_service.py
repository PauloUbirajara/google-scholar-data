from scholarly import scholarly

from src.types.scholar_info import ScholarInfo


class ScholarlyService:
	def fetch_info(id: str) -> ScholarInfo:
		result = scholarly.search_author_id(id)
		full_author_info = scholarly.fill(result)

	"citedby": 428,
  "organization": 6518679690484165796,
  "homepage": "http://steven.cholewiak.com/",
  "citedby5y": 292,
  "hindex": 10,
  "hindex5y": 10,
  "i10index": 10,
  "i10index5y": 10,
  "


		info = ScholarInfo(
			current_year_citations=full_author_info.get('citedby'),
			h10_index=full_author_info.get(''),
		)
		return info
		

# from scholarly import scholarly

# # Retrieve the author's data, fill-in, and print
# # Get an iterator for the author results
# search_query = scholarly.search_author('Steven A Cholewiak')
# # Retrieve the first result from the iterator
# first_author_result = next(search_query)
# scholarly.pprint(first_author_result)

# # Retrieve all the details for the author
# author = scholarly.fill(first_author_result )
# scholarly.pprint(author)

# # Take a closer look at the first publication
# first_publication = author['publications'][0]
# first_publication_filled = scholarly.fill(first_publication)
# scholarly.pprint(first_publication_filled)

# # Print the titles of the author's publications
# publication_titles = [pub['bib']['title'] for pub in author['publications']]
# print(publication_titles)

# # Which papers cited that publication?
# citations = [citation['bib']['title'] for citation in scholarly.citedby(first_publication_filled)]
# print(citations)