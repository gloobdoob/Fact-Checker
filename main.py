#!/usr/bin/env python
# coding: utf-8

# In[5]:
import os
from image_reader import ImageReader
from text_corrector import TextCorrector
from similarity_checker import SimilarityChecker
from google_scraper import GoogleScraper



def main():
    path = 'news dataset/real'
    imgs = os.listdir(path)
    img = os.path.join(path, imgs[2])

    ocr = ImageReader()
    text = ocr.read_img(img)

    c = TextCorrector()
    corrected = c.correct(text)
    article = c.decide_text(text, corrected)

    g = GoogleScraper()
    s = SimilarityChecker()

    if len(text) > 5:
        summarized = c.summarize(article)
        s_result = g.get_results(summarized)
        search_titles = [title[0] for title in s_result]
        search_links = [title[1] for title in s_result]
        sim_rating = s.check_similarity(summarized, search_titles, links=search_links)
        print(sim_rating)

    else:
        s_result = g.get_results(article)
        search_titles = [title[0] for title in s_result]
        search_links = [title[1] for title in s_result]
        sim_rating = s.check_similarity(article, search_titles, links=search_links)
        print(sim_rating)

if __name__ == "__main__":
    main()




