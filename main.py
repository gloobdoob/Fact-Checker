import os
from image_reader import ImageReader
from text_corrector import TextCorrector
from similarity_checker import SimilarityChecker
from google_scraper import GoogleScraper
from knapsack_checker import KnapsackChecker

class SearchResultException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

def check(text, c, gs, sc):
    query = None
    # if the text is not that long, it will not summarize
    if len(text) > 45:
        query = c.summarize(text)

    else:
        query = text

    print('To search:', query)

    s_result = gs.get_results(query)
    if s_result:
        search_title = [title[0] for title in s_result]
        search_body = [title[1] for title in s_result]
        search_links = [title[2] for title in s_result]
        #print("checking similarities")
        sim_rating_title = sc.check_similarity(query, search_title)
        sim_rating_body = sc.check_similarity(query, search_body)
        # print(len(s_result))
        return sim_rating_title, sim_rating_body, search_links

    else:
        raise SearchResultException()

def main(img):
    ocr = ImageReader()
    text = ocr.read_img(img)
    print("extracted:", text)

    c = TextCorrector()
    corrected = c.correct(text)
    article = c.decide_text(text, corrected)

    gs = GoogleScraper()
    sc = SimilarityChecker()


    t_sim_rating, b_sim_rating, urls = check(article, c, gs, sc)
    kc = KnapsackChecker(t_sim_rating, urls)
    res_url_wts, res_sim, full_res_sites = kc.checker()
    print(res_sim)
    pred = kc.truth_checker_k(res_sim, len(res_url_wts))

    return pred, full_res_sites, urls

if __name__ == "__main__":
    # path for image, this is where you add your image
    # for the dropbox thing
    img_path = 'news dataset/real/271461659_1115525192528967_385823889246825612_n.jpg'

    # u can erase these two lines
    # ------------
    # imgs = os.listdir(path)
    # img = os.path.join(path, imgs[6])
    # -------------

    prediction, sites, urls = main(img_path)
    if prediction == 'Real':
        print('We predict that this is', prediction)
        print('These are the articles from credible sites that we ran across when searching for this image: ')
        print(sites)
    elif prediction == 'Risky' and sites:
        print('We predict that this is', prediction + '.', 'Please do more research regarding this topic')
        print('These are the articles from credible sites that we ran across when searching for this image: ')
        print(sites)
    elif prediction == 'Risky' and not sites:
        print('We predict that this is a', prediction + ' article.', 'Please do more research regarding this topic')
        print('There were no credible websites that appeared while searching for this image')
        print('These are the risky websites that came up when searching: ')
        print(urls)






