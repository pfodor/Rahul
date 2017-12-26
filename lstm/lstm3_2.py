import torch
import torch.nn as nn
from torch.autograd import Variable
import sys
from random import shuffle

NUM_EXAMPLES=1000

train_input = ['{0:020b}'.format(i) for i in range(2**20)]
shuffle(train_input)
train_input = [map(int,i) for i in train_input]
ti  = []
for i in train_input:
    temp_list = []
    for j in i:
            temp_list.append(j)
    #ti.append(np.array(temp_list))
    ti.append([[temp_list]])
train_input = ti

train_output = []
for x in train_input:
    count = 0
    for i in x:
        i = i[0]
        for j in i:
            if j == 1:
                count+=1
            #temp_list = ([0]*21)
            #temp_list[count]=1
        temp_list=[count]
        train_output.append(temp_list)

test_input = train_input[NUM_EXAMPLES:]
test_output = train_output[NUM_EXAMPLES:]
train_input = train_input[:NUM_EXAMPLES]
train_output = train_output[:NUM_EXAMPLES]
#for x in range(len(train_input)):
#    print(train_input[x], " ====== ", train_output[x])
#sys.exit()
epoch = 5000

in_size = 20
classes_no = 20 #hidden states

model = nn.LSTM(in_size, classes_no, 1)
loss = nn.CrossEntropyLoss()

for x in range(epoch):
    print("epoch: ", x)
    for i in range(len(train_input[0])):
        input_seq=Variable(torch.Tensor(train_input[0]))
        #print(input_seq)
        #hidden = (Variable(torch.randn(1, 1, 20)),
        #          Variable(torch.randn((1, 1, 20))))
        output_seq, _ = model(input_seq)
        last_output = output_seq[-1]
        #print(output_seq)
        #print('\n')
        #print(last_output)
        #print()
        _, predicted = torch.max(output_seq.data, 1)
        #print(predicted)
        target = Variable(torch.LongTensor(train_output[0]))
        #print(target)
        #print()
        #print(predicted)
        err = loss(last_output, target)
        err.backward()
    print("epoch: ", x, "error: ", err)

total = len(test_input)
correct = 0
for x in range(len(test_input)):
    input_seq = Variable(torch.Tensor(test_input[x]))
    #hidden = (Variable(torch.randn(1, 1, 20)),
    #          Variable(torch.randn((1, 1, 20))))
    output_seq, _ = model(input_seq)
    last_output = output_seq[-1]
    pred = last_output.data.max(1, keepdim=True)[1]
    print("pred:  ",  pred[0][0], "--------   test_output:  ",test_output[x][0] )
    if pred[0][0] == test_output[x][0]:
        correct +=1

print(correct/total)



