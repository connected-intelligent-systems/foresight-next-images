import numpy as np
import pandas as pd
import torch
import torch.utils.data as data_utils


class NILMDataset(data_utils.Dataset):
    def __init__(self, x, y, status, window_size=480, stride=30):
        self.x = x
        self.y = y
        self.status = status
        self.window_size = window_size
        self.stride = stride

    def __len__(self):
        return int(np.ceil((len(self.x) - self.window_size) / self.stride) + 1)

    def __getitem__(self, index):
        start_index = index * self.stride
        end_index = np.min((len(self.x), index * self.stride + self.window_size))


        x = self.padding_seqs(self.x[start_index: end_index])
        y = self.padding_seqs(self.y[start_index: end_index])
        status = self.padding_seqs(self.status[start_index: end_index])


        if isinstance(x, pd.Series):
            x = x.values
        if isinstance(y, pd.Series):
            y = y.values
        if isinstance(status, pd.Series):
            status = status.values


        x = torch.tensor(x).view((1, -1))
        y = torch.tensor(y).view((1, -1))
        status = torch.tensor(status).view((1, -1))

        return x, y, status  # [1, window_size], [1, window_size], [1, window_size]

    def padding_seqs(self, in_array):
        if len(in_array) == self.window_size:
            return in_array
        try:
            out_array = np.zeros((self.window_size, in_array.shape[1]))
        # except Exception as e:
        except:
            # print(f'last batch does not have enough elements i.e. {self.window_size} and has {in_array.shape[1]} elements')
            out_array = np.zeros(self.window_size)

        out_array[:len(in_array)] = in_array
        return out_array
