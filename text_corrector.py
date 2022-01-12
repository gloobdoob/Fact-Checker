from transformers import pipeline
from happytransformer import HappyTextToText, TTSettings
from similarity_checker import SimilarityChecker

class TextCorrector:
    def __init__(self):
        self.summarizer = pipeline(model='sshleifer/distilbart-cnn-12-6')
        self.happy_tt = HappyTextToText("T5", "prithivida/grammar_error_correcter_v1")
        self.sim_checker = SimilarityChecker()

    def correct(self, text):
        print("corrected")
        args = TTSettings(do_sample=True, top_k=20, temperature=0.7, min_length=1, max_length=100, early_stopping=True)
        sentence = self.happy_tt.generate_text(text, args=args).text

        return sentence

    def summarize(self, text):
        text_len = (len(text.split()) + len(text.split()) - 1)
        article = text
        summary = self.summarizer(article, min_length=int(0.1 * len(text)), max_length=int(0.3 * len(text)),
                                  do_sample=False, num_beams=4, early_stopping=True)
        print("summarized")
        return summary[0]['summary_text']

    def decide_text(self, text, corrected):
        article = None
        sim_rating = self.sim_checker.check_similarity(text, corrected)[0]
        if sim_rating > 0.75:
            article = corrected
            print(sim_rating)
        else:
            article = text

        return article
