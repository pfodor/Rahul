""" Dynamic Recurrent Neural Network.

TensorFlow implementation of a Recurrent Neural Network (LSTM) that performs
dynamic computation over sequences with variable length. This example is using
a toy dataset to classify linear sequences. The generated sequences have
variable length.

Links:
    [Long Short Term Memory](http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf)

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
"""

from __future__ import print_function

import os
import tensorflow as tf 
import random
import sys
import string


def stringTranslation(s):

    d={}
    #x = string.ascii_lowercase+string.ascii_uppercase+'123456789'
    x=string.ascii_letters+string.digits
    r=150-len(x)
    point = 161
    for j in range(r):
        x+=chr(point)
        point+=1

    i = 1
    
    for q in x:
        d[q]=i
        i+=1

    ret=[]
    for l in s:
        ret.append([d[l]])
    return ret

def padData(a, max_len=50):

    ret = a
    slen = len(a)
    ret +=[[0] for i in range(max_len-slen)]
    return ret


class RenderSequenceData(object):
    
    def __init__(self, sl, traindir, testdir, max_seqlen=50):
        
        self.train_data = []
        self.train_labels = []
        self.train_seqlen = []

        self.test1_data=[]
        self.test1_labels = []
        self.test1_seqlen = []

        self.test2_data=[]
        self.test2_labels = []
        self.test2_seqlen = []

        trainPFile = open(traindir+'Training_'+sl+'_positive.txt','r')
        trainNFile = open(traindir+'Training_'+sl+'_negative.txt','r')

        test1PFile = open(testdir+'test1_'+sl+'_positive.txt', 'r')
        test1NFile = open(testdir+'test1_'+sl+'_negative.txt', 'r')

        test2PFile = open(testdir+'test2_'+sl+'_positive.txt', 'r')
        test2NFile = open(testdir+'test2_'+sl+'_negative.txt', 'r')

        #gather training data from file
        stringPosDict={}
        stringNegDict={}

        for i in trainPFile:
            x = i[:-1]
            if len(x) in stringPosDict:
                stringPosDict[len(x)].append(x)
            else:
                stringPosDict[len(x)]=[x]
                
        for i in trainNFile:
            x = i[:-1]
            if len(x) in stringNegDict:
                stringNegDict[len(x)].append(x)
            else:
                stringNegDict[len(x)]=[x]

        totalStrings = 0
        for i in stringPosDict:
            totalStrings+=len(stringPosDict[i])
        for i in stringNegDict:
            totalStrings+=len(stringNegDict[i])

        key = 1
        while len(self.train_data) < totalStrings:
            x = random.randint(0,1)
            if x == 1:
                if key in stringPosDict and stringPosDict[key] != []:
                    a = stringPosDict[key].pop(0)
                    t = stringTranslation(a)
                    t = padData(t)
                    self.train_data.append(t)
                    self.train_labels.append([1,0])
                    self.train_seqlen.append(len(a))
            else:
                if key in stringNegDict and stringNegDict[key] != []:
                    a = stringNegDict[key].pop(0)
                    t = stringTranslation(a)
                    t = padData(t)
                    self.train_data.append(t)
                    self.train_labels.append([0,1])
                    self.train_seqlen.append(len(a))
            if key not in stringPosDict or stringPosDict[key] == []:
                if key not in stringNegDict or stringNegDict[key] == []:
                    key+=1

        ##acquire test data
        stringPosDict={}
        stringNegDict={}
        for i in test1PFile:
            x = i[:-1]
            if len(x) in stringPosDict:
                stringPosDict[len(x)].append(x)
            else:
                stringPosDict[len(x)]=[x]
                
        for i in test1NFile:
            x = i[:-1]
            if len(x) in stringNegDict:
                stringNegDict[len(x)].append(x)
            else:
                stringNegDict[len(x)]=[x]

        for i in stringPosDict:
            totalStrings+=len(stringPosDict[i])
        for i in stringNegDict:
            totalStrings+=len(stringNegDict[i])

        i = 0
        while i<51:
            if i in stringPosDict:
                for x in stringPosDict[i]:
                    t = stringTranslation(x)
                    t = padData(t)
                    self.test1_data.append(t)
                    self.test1_labels.append([1,0])
                    self.test1_seqlen.append(len(x))
            if i in stringNegDict:
                for x in stringNegDict[i]:
                    t = stringTranslation(x)
                    t = padData(t)
                    self.test1_data.append(t)
                    self.test1_labels.append([0,1])
                    self.test1_seqlen.append(len(x))
            i+=1

        stringPosDict={}
        stringNegDict={}

        for i in test2PFile:
            x = i[:-1]
            if len(x) in stringPosDict:
                stringPosDict[len(x)].append(x)
            else:
                stringPosDict[len(x)]=[x]
                
        for i in test2NFile:
            x = i[:-1]
            if len(x) in stringNegDict:
                stringNegDict[len(x)].append(x)
            else:
                stringNegDict[len(x)]=[x]

        i = 0
        while i<51:
            if i in stringPosDict:
                for x in stringPosDict[i]:
                    t = stringTranslation(x)
                    t = padData(t)
                    self.test2_data.append(t)
                    self.test2_labels.append([1,0])
                    self.test2_seqlen.append(len(x))
            if i in stringNegDict:
                for x in stringNegDict[i]:
                    t = stringTranslation(x)
                    t = padData(t)
                    self.test2_data.append(t)
                    self.test2_labels.append([0,1])
                    self.test2_seqlen.append(len(x))
            i+=1
        
        self.batch_id = 0

    def next(self, batch_size):
        """ Return a batch of data. When dataset end is reached, start over.
        """
        if self.batch_id == len(self.data):
            self.batch_id = 0
        batch_data = (self.data[self.batch_id:min(self.batch_id +
                                                  batch_size, len(self.data))])
        batch_labels = (self.labels[self.batch_id:min(self.batch_id +
                                                  batch_size, len(self.data))])
        batch_seqlen = (self.seqlen[self.batch_id:min(self.batch_id +
                                                  batch_size, len(self.data))])
        self.batch_id = min(self.batch_id + batch_size, len(self.data))
        return batch_data, batch_labels, batch_seqlen


# ==========
#   MODEL
# ==========

# Parameters
learning_rate = 0.01

# Network Parameters
seq_max_len = 50 # Sequence max length
n_hidden = int(sys.argv[3]) # hidden layer num of features
n_classes = 2 # linear sequence or not

sl= sys.argv[1]  #'SL2'
k_chunk = sys.argv[2] #'1k'
traindir = sys.argv[4]+'/'+k_chunk+'/' #'../sl_train56/1k/'
testdir = sys.argv[5]+'/'+k_chunk+'/'  #'../sl_test56/1k/'

dataset = RenderSequenceData(sl,traindir, testdir)

#x = dataset.train_data[0:30]
#y = dataset.train_labels[0:30]
#s = dataset.train_seqlen[0:30]
#print(x,'\n\n\n',y,'\n\n\n',s)
#sys.exit()

#testset = ToySequenceData(n_samples=500, max_seq_len=seq_max_len)

# tf Graph input
x = tf.placeholder("float", [None, seq_max_len, 1])
y = tf.placeholder("float", [None, n_classes])
# A placeholder for indicating each sequence length
seqlen = tf.placeholder(tf.int32, [None])

# Define weights
weights = {
    'out': tf.Variable(tf.random_normal([n_hidden, n_classes]))
}
biases = {
    'out': tf.Variable(tf.random_normal([n_classes]))
}


def dynamicRNN(x, seqlen, weights, biases):

    # Prepare data shape to match `rnn` function requirements
    # Current data input shape: (batch_size, n_steps, n_input)
    # Required shape: 'n_steps' tensors list of shape (batch_size, n_input)
    
    # Unstack to get a list of 'n_steps' tensors of shape (batch_size, n_input)
    x = tf.unstack(x, seq_max_len, 1)

    # Define a lstm cell with tensorflow
    lstm_cell = tf.contrib.rnn.BasicLSTMCell(n_hidden)

    # Get lstm cell output, providing 'sequence_length' will perform dynamic
    # calculation.
    outputs, states = tf.contrib.rnn.static_rnn(lstm_cell, x, dtype=tf.float32,
                                sequence_length=seqlen)

    # When performing dynamic calculation, we must retrieve the last
    # dynamically computed output, i.e., if a sequence length is 10, we need
    # to retrieve the 10th output.
    # However TensorFlow doesn't support advanced indexing yet, so we build
    # a custom op that for each sample in batch size, get its length and
    # get the corresponding relevant output.

    # 'outputs' is a list of output at every timestep, we pack them in a Tensor
    # and change back dimension to [batch_size, n_step, n_input]
    outputs = tf.stack(outputs)
    outputs = tf.transpose(outputs, [1, 0, 2])

    # Hack to build the indexing and retrieve the right output.
    batch_size = tf.shape(outputs)[0]
    # Start indices for each sample
    index = tf.range(0, batch_size) * seq_max_len + (seqlen - 1)
    # Indexing
    
    outputs = tf.gather(tf.reshape(outputs, [-1, n_hidden]), index)

    # Linear activation, using outputs computed above
    return tf.matmul(outputs, weights['out']) + biases['out']

pred = dynamicRNN(x, seqlen, weights, biases)
# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)

# Evaluate model
correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()

train_input = dataset.train_data
batch_size = 128
no_of_batches = int((len(train_input)) / batch_size)
epoch = 100
# Start training
with tf.Session() as sess:

    # Run the initializer
    sess.run(init)

    for i in range(epoch):
        ptr = 0
        for j in range(no_of_batches):
            batch_x = dataset.train_data[ptr:ptr+batch_size]
            batch_y = dataset.train_labels[ptr:ptr+batch_size]
            batch_seqlen = dataset.train_seqlen[ptr:ptr+batch_size]
            # Run optimization op (backprop)
            sess.run(optimizer, feed_dict={x: batch_x, y: batch_y,
                                           seqlen: batch_seqlen})
        #print("Epoch: ",str(i))

    # Calculate accuracy
    test1_data = dataset.test1_data
    test1_label = dataset.test1_labels
    test1_seqlen = dataset.test1_seqlen

    test2_data = dataset.test2_data
    test2_label = dataset.test2_labels
    test2_seqlen = dataset.test2_seqlen


    print("*",sl, str(k_chunk)+'k')
    print("* Test1 Accuracy:", \
        sess.run(accuracy, feed_dict={x: test1_data, y: test1_label, seqlen: test1_seqlen}))

    print("* Test2 Accuracy:", \
        sess.run(accuracy, feed_dict={x: test2_data, y: test2_label, seqlen: test2_seqlen}))
