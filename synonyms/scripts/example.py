from synonyms.dictionary import Dictionary
from synonyms.synonyms import SVDModel

dictionary = Dictionary(filename='dictionary_filename')
# U = ... load U matrix
# s = ... load s matrix
model = SVDModel(U, s, dictionary)
model.dimensions = 2500
model.caron_p = 0.25
synonyms, ids, score = model.get_synonyms('target_word', 10, return_ids=True, return_score=True)
