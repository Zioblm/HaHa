from fastcoref import FCoref


def coref_resolution(text):
    corefmodel = FCoref(device='cuda:0')
    sequence_to_coref = []
    sequence_to_coref.append(text)
    preds=corefmodel.predict(texts=sequence_to_coref)

    # fetches tokens with whitespaces from spacy document
    tok_list = preds[0].get_clusters(True)
    for pair in tok_list:
        entity = pair[0]  
        for mention in pair:
            if len(entity)>len(mention):
               text = text.replace(mention,entity)
    return text