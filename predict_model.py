import pandas as pd
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertForMaskedLM
import numpy as np

all_data = pd.read_csv('train_full.csv')
model_name = "DeepPavlov/rubert-base-cased"
fine_tune = "model"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForMaskedLM.from_pretrained(model_name)
model.load_state_dict(torch.load(fine_tune))


def get_response(user_answer: str, question: str):
    answers = all_data[all_data['Question'] == question]['Answer'].values
    target = all_data[all_data['Question'] == question]['Correctness'].values
    scores = []

    for answer in answers:
        tokens1 = tokenizer.encode(user_answer, add_special_tokens=True)
        tokens2 = tokenizer.encode(answer, add_special_tokens=True)
        input_ids1 = torch.tensor([tokens1])
        input_ids2 = torch.tensor([tokens2])

        with torch.no_grad():
            outputs1 = model.bert(input_ids1)
            outputs2 = model.bert(input_ids2)

            embeddings1 = outputs1.last_hidden_state.mean(dim=1)
            embeddings2 = outputs2.last_hidden_state.mean(dim=1)

        similarity = cosine_similarity(embeddings1, embeddings2)
        scores.append(similarity[0][0])

    res = np.argpartition(scores, -2)[-2:]
    predictions = target[res]

    # print(scores)
    # print(target)
    # print(predictions)

    #check kNN
    if sum(predictions) == 0:
        return 'Вы ошиблись! '

    #check threshold
    flag = False
    if predictions[0] == 1:
        flag = scores[res[0]] > 0.7
    if predictions[1] == 1 and not flag:
        flag = scores[res[1]] > 0.7

    if not flag:
        return 'Вы ошиблись! '

    return 'Все верно! '
