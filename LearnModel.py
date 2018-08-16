#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parts of the code herein were
inspried by original code at cognitiveclass.ai
it can be found here (but you may have go sign up):
https://courses.cognitiveclass.ai/courses/course-v1:CognitiveClass+ML0120ENv2+2018/courseware/89227024130b43f684d95376901b65c8/e7c36d2c4c6840fe8b81b97147ea9c16/

I have marked _their_ code with #CCAI.
I have marked _their comments_ with #CCOM
"""


import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

"""
CCOM
Next, let's start building our RBM with Tensorflow.
We'll begin by first determining the amount of hidden layers
and then creating placeholder variables for storing our visible layer biases,
hidden layer biases and weights that connect the hidden layer with the visible one.
We will be arbitrarily setting the amount of hidden layers to 20.
You can freely set this value to any number you want since each neuron in the hidden
layer will end up learning a feature.
"""
def buildviewinghabits(sess,trX,hiddenUnits, visibleUnits):
    vb = tf.placeholder("float", [visibleUnits]) #CCAI: Number of unique movies
    hb = tf.placeholder("float", [hiddenUnits]) #CCAI: Number of features we're going to learn
    W = tf.placeholder("float", [visibleUnits, hiddenUnits])
    """
    CCOM
    We then move on to creating the visible and hidden layer units
    and setting their activation functions. In this case, we will
    be using the tf.sigmoid and tf.relu functions as nonlinear activations
    since it's what is usually used in RBM's.
    """
    #CCAI: Phase 1: Input Processing
    v0 = tf.placeholder("float", [None, visibleUnits])
    _h0= tf.nn.sigmoid(tf.matmul(v0, W) + hb)
    h0 = tf.nn.relu(tf.sign(_h0 - tf.random_uniform(tf.shape(_h0))))
    """
    CCOM
    initialize our variables
    """
    #CCAI: Current weight
    cur_w = np.zeros([visibleUnits, hiddenUnits], np.float32)
    #CCAI: Current visible unit biases
    cur_vb = np.zeros([visibleUnits], np.float32)
    #CCAI: Current hidden unit biases
    cur_hb = np.zeros([hiddenUnits], np.float32)
    #CCAI: Phase 2: Reconstruction
    _v1 = tf.nn.sigmoid(tf.matmul(h0, tf.transpose(W)) + vb)
    v1 = tf.nn.relu(tf.sign(_v1 - tf.random_uniform(tf.shape(_v1))))
    h1 = tf.nn.sigmoid(tf.matmul(v1, W) + hb)
    """
    CCOM
    Now we set the RBM training parameters and functions.
    """
    #CCAI: Learning rate
    alpha = 1.0
    #CCAI: Create the gradients
    w_pos_grad = tf.matmul(tf.transpose(v0), h0)
    w_neg_grad = tf.matmul(tf.transpose(v1), h1)
    #CCAI: Calculate the Contrastive Divergence to maximize
    CD = (w_pos_grad - w_neg_grad) / tf.to_float(tf.shape(v0)[0])
    #CCAI: Create methods to update the weights and biases
    update_w = W + alpha * CD
    update_vb = vb + alpha * tf.reduce_mean(v0 - v1, 0)
    update_hb = hb + alpha * tf.reduce_mean(h0 - h1, 0)
    """
    CCOM
    And set the error function, which in this case will be the Mean Absolute Error Function.
    """
    err = v0 - v1
    err_sum = tf.reduce_mean(err * err)#PM just reducing mena square error



    """
    CCOM (PM note: numbers subject to change)
    Now we train the RBM with
    15 epochs with each epoch using
    10 batches with size 100.
    After training, we print out a graph with the error by epoch.
    """
    epochs = 999#PM changed from 15 to try and remove inconsistency in results
    batchsize = 100
    errors = []
    for i in range(epochs):
        for start, end in zip( range(0, len(trX), batchsize), range(batchsize, len(trX), batchsize)):
            batch = trX[start:end]
#            prv_w = cur_w #order of operation reversed because
#            prv_vb = cur_vb
#            prv_hb = cur_hb
            cur_w = sess.run(update_w, feed_dict={v0: batch, W: cur_w, vb: cur_vb, hb: cur_hb})
            cur_vb = sess.run(update_vb, feed_dict={v0: batch, W: cur_w, vb: cur_vb, hb: cur_hb})
            cur_hb = sess.run(update_hb, feed_dict={v0: batch, W: cur_w, vb: cur_vb, hb: cur_hb})

        errors.append(sess.run(err_sum, feed_dict={v0: trX, W: cur_w, vb: cur_vb, hb: cur_hb}))
        lasterr=errors[-1]
        if lasterr<0.033:
            print("breaking at " + str(i))
            break
        print (lasterr)
    plt.plot(errors)
    plt.ylabel('Error')
    plt.xlabel('Epoch')
    plt.show()

    return cur_w, cur_vb, cur_hb, W, vb, hb, v0

