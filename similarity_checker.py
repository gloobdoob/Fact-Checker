from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option("display.max_columns", 10)


class SimilarityChecker:
    def __init__(self):
        self.comp_model = SentenceTransformer('bert-base-nli-mean-tokens')

    def check_similarity(self, orig_text, comp_list, links=None):
        orig_text_embeddings = self.comp_model.encode(orig_text)
        comp_text_embeddings = self.comp_model.encode(comp_list)

        if isinstance(comp_list, list):
            sim_rating = cosine_similarity(
                [orig_text_embeddings],
                comp_text_embeddings
            )
            sentence_dict = {'Original Text Extracted': orig_text, 'Headlines': comp_list, 'Links': links,
                             'Similarity Rating': sim_rating[0]}
            df = pd.DataFrame(sentence_dict)
            return df

        else:
            sim_rating = cosine_similarity(
                [orig_text_embeddings],
                [comp_text_embeddings]
            )
            return sim_rating[0]
