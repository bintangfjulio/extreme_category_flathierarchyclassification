import torch.nn as nn
import pytorch_lightning as pl

from transformers import BertModel

class BERT(pl.LightningModule):
    def __init__(self, num_classes, dropout=0.1, input_size=768, hidden_size=768):
        super(BERT, self).__init__()
        self.bert = BertModel.from_pretrained('indolem/indobert-base-uncased')
        self.linear_layer = nn.Linear(input_size, hidden_size)
        self.fully_connected = nn.Linear(hidden_size, num_classes)
        self.dropout = nn.Dropout(dropout)   
        self.tanh = nn.Tanh()

    def forward(self, input_ids):
        bert_output = self.bert(input_ids=input_ids)
        last_hidden_state = bert_output[0]
        cls_hidden_state = last_hidden_state[:, 0]
        pooler = self.linear_layer(cls_hidden_state)
        pooled_output = self.tanh(pooler)
        output = self.fully_connected(self.dropout(pooled_output))

        return output
