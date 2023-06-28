def extract_tag(ancestor,selector=None, attribute=None, return_list=False):
    try:
        if return_list:
            return [tag.text.strip() for tag in ancestor.select(selector)]
        if not selector and attribute:
            return ancestor[attribute]
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).text.strip()
    except (AttributeError, TypeError):
        return None
    
selectors = {
        "ID_Opinii": [None,"data-entry-id"],
        "Autor" : ["span.user-post__author-name"],
        "Polecenie" : ["span.user-post__author-recomendation > em"],
        "Ocena" : ["span.user-post__score-count"],
        "Weryfikacja" : ["div.review-pz"],
        "Data publikacji" : ["span.user-post__published > time:nth-child(1)","datetime"],
        "Data zakupu" : ["span.user-post__published > time:nth-child(2)","datetime"],
        "Przydatnosc" : ["button.vote-yes","data-total-vote"],
        "Nieprzydatnosc" : ["button.vote-no","data-total-vote"],
        "Zawartosc" : ["div.user-post__text"],
        "Wady" : ["div.review-feature__title--negatives ~ div.review-feature__item", None, True],
        "Zalety" : ["div.review-feature__title--positives ~ div.review-feature__item", None, True],
}
