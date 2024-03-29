# -*- coding: utf-8 -*-
import pickle

char_to_ix = pickle.load(open("chardict_sentsplit.pickle", "rb"))
# print(char_to_ix)

tag_to_ix = {'N':0, 'S':1}

import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.manual_seed(1)

class LSTMTagger(nn.Module):

    def __init__(self, embedding_dim, hidden_dim, vocab_size, tagset_size):
        super(LSTMTagger, self).__init__()
        self.hidden_dim = hidden_dim
        #self.batch_size = batch_size

        self.char_embeddings = nn.Embedding(vocab_size, embedding_dim)

        # The LSTM takes word embeddings as inputs, and outputs hidden states
        # with dimensionality hidden_dim.
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, bidirectional=True)  # <- change here

        # The linear layer that maps from hidden state space to tag space
        self.hidden2tag = nn.Linear(hidden_dim * 2, tagset_size)

    def forward(self, sentence):
        embeds = self.char_embeddings(sentence)
        lstm_out, _ = self.lstm(embeds.view(len(sentence), 1, -1))
        tag_space = self.hidden2tag(lstm_out.view(len(sentence), -1))
        tag_scores = F.log_softmax(tag_space, dim=1)
        return tag_scores

model = LSTMTagger(300, 256, len(char_to_ix), len(tag_to_ix))
loss_function = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr = 0.1)

model_save_name = '24082022_sentencesplitter_emb300_hid256_epoch20.pt'

model.load_state_dict(torch.load(model_save_name))

def prepare_sequence(seq, to_ix):
  idxs = [to_ix[ch] for ch in seq]
  return torch.tensor(idxs, dtype = torch.long)

def prob_to_tag(probs):
  _sentence_tag_list = []
  #for sentence in tag_scores
  _prob_to_tag = []
  for ch in probs:
      chlist = list(ch)
      #print(chlist)
      maxi = max(chlist)
      ind = chlist.index(maxi)  
      _prob_to_tag.append((list(tag_to_ix.keys())[ind]))
  _sentence_tag_list.append(_prob_to_tag)
  return _sentence_tag_list

def _char_to_token(samplesent, _sentence_tag_list):
    token_list = []
    token = []
    for j in range(len(_sentence_tag_list[0])): #for each character of a sentence
        ch = _sentence_tag_list[0][j]
        ach = samplesent[j]

        if ch == 'N':
          token.append(ach)
          

        else:
          if ch =='S':
            token.append(ach)
            token_list.append(token)
            token=[]
   
    
    return token_list

def char_unifier(_token_list):
  for item in range(len(_token_list)):
    
      _token_list[item]= ''.join(_token_list[item])
  return _token_list

def sentence_splitter(sentence):
  input = prepare_sequence(sentence, char_to_ix)
  probs = model(input)
  sentence_tag_list = prob_to_tag(probs)
  token_list = _char_to_token(sentence, sentence_tag_list)
  out = char_unifier(token_list)
  return out

samplesent = "Filmde kamburunu çıkarmış eski Yugoslav lideri, iki kişinin arasında elleri önden bağlı, cezaevi avlusunda yürüyor.Sabahları hiçbir şey yemeden içmeden, paldür küldür çıkıyorum evden."

print(sentence_splitter(samplesent))
