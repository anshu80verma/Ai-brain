import json
import torch
import torch.nn as nn
from torch.utils.data import dataset ,dataloader
from NerualNetworking import bag_of_words , tokenize , stem
from Brain import NerualNet
import numpy as np

with open('intents.json','r') as  f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    
    for pattern in intent['patterns']:
        print(pattern)
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w,tag))

ignore_words = [',','?','!','.','/']
all_words = [stem(w) for w in all_words if w not in ignore_words]   
all_words = sorted(set(all_words))
tag = sorted(set(tag))

x_train = []
y_tarin  = []

for(pattern_sentence , tag) in xy:
    bag = bag_of_words(pattern_sentence,all_words)
    x_train.append(bag)
    label = tags.index(tag)
    y_tarin.append(label)

x_train = np.array(x_tarin)
y_train = np.array(y_train)

num_epochs =1000
batch_size = 8
learning_rate = 0.001
hidden_size = 8
input_size = len(x_train[0])
output_size = len(tags)

print("Train the model...")


class chatDataset(dataset):
    def __init__(self):
        self.n_samples = len(x_train)
        self.x_data  = x_train
        self.y_data = y_train


    def __getitem__(self,index):
        return self.x_data[index],self.y_data[index]


    def __len__(self):
        return self.n_samples


Dataset = chatDataset()

train_loader = dataloader(dataset = dataset,batch_size = batch_size,shuffle = True , num_worker = 0)
Device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model  =    NerualNet(input_size,hidden_size,output_size).to(device=Device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr = learning_rate)
    
