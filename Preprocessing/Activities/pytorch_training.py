import torch
import torch.nn.functional as F
from torch.utils.data import Dataset
from sklearn.preprocessing import LabelEncoder

import joblib
import pandas as pd
import numpy as np


def get_device():
    if torch.cuda.is_available():
        device = torch.device('cuda:0')
    else:
        device = torch.device('cpu')  # don't have GPU
    return device


class CustomDataset(Dataset):
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv('./resources/coordinates.csv')
        ys = self.df['0']
        ys = ys.values.tolist()
        label_encoder = LabelEncoder()
        ys = np.expand_dims(label_encoder.fit_transform(ys), axis=1)
        # labels = torch.nn.functional.one_hot(torch.from_numpy(labels)).cpu().detach().numpy()
        with open('./resources/label_encoder.sav', 'wb') as f:
            joblib.dump(label_encoder, f)
        features = self.df.drop('0', axis=1).values
        self.data = np.concatenate((ys, features), axis=1)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        data_instance = self.data[index]
        self.y = int(data_instance[0])
        self.x = np.float32(np.delete(data_instance, 0))
        return self.x, self.y


batch_size = 32
dataset = CustomDataset()
train_size = np.int(len(dataset) * 0.8)
train_set, test_set = torch.utils.data.random_split(dataset, [train_size, len(dataset) - train_size])
train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=2)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size, shuffle=True, num_workers=2)


# exit()
class Net(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = torch.nn.Linear(300, 300, bias=True)
        self.fc2 = torch.nn.Linear(300, 300, bias=True)
        self.out = torch.nn.Linear(300, 4) # activity classes: eating, ordering, requsting_bill, paying_bill

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.softmax(self.out(x))
        return x


net = Net()

loss_function = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters(), lr=0.0001)

for epoch in range(10):
    running_loss = 0.0
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data

        optimizer.zero_grad()

        outputs = net(inputs)
        loss = loss_function(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if i % 100 == 99:
            print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
            running_loss = 0.0
print('finished training!')

torch.save(net.state_dict(), 'model.pt')
