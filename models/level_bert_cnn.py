import torch
import torch.nn as nn
import torch.nn.functional as F

from transformers import BertModel

class Level_BERT_CNN(nn.Module):
    def __init__(self, bert_model, dropout, input_size=768, window_sizes=[1, 2, 3, 4, 5], in_channels=4, out_channels=32):
        super(Level_BERT_CNN, self).__init__()
        self.pretrained_bert = BertModel.from_pretrained(bert_model, output_hidden_states=True)
        self.convolutional_layers = nn.ModuleList([nn.Conv2d(in_channels, out_channels, (window_size, input_size)) for window_size in window_sizes])
        self.dropout = nn.Dropout(dropout) 
        self.window_len = len(window_sizes)
        self.out_channels_len = out_channels

    def forward(self, input_ids):
        bert_output = self.pretrained_bert(input_ids=input_ids)
        bert_hidden_states = bert_output[2]
        bert_hidden_states = torch.stack(bert_hidden_states, dim=1)
        selected_hidden_states = bert_hidden_states[:, -4:]

        pooler = [F.relu(layer(selected_hidden_states).squeeze(3)) for layer in self.convolutional_layers] 
        max_pooler = [F.max_pool1d(features, features.size(2)).squeeze(2) for features in pooler]  

        flatten = torch.cat(max_pooler, dim=1) 
        logits = self.dropout(flatten)
        
        return logits
    
    def get_window_length(self):
        return self.window_len
    
    def get_out_channels_length(self):
        return self.out_channels_len