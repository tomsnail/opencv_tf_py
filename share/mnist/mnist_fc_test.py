# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import cv2
import os
import math



def readData(path,filename):
    images = np.empty((1, 28 * 28), dtype=np.float32)
    label = np.zeros((1,10), dtype=np.float32)

    img = cv2.imread(path)
    img = cv2.resize(img, (28, 28))
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #img = (img - (255 / 1.0)) / 255
    # cv2.imshow(filename,img)
    # cv2.waitKey()
    tva = [0*x for x in range(28*28)]
    for i in range(28):
        for j in range(28):
            tva[i * 28 + j] = math.fabs((0 - img[i][j])) * 1.0 / 255.0

    images[0, :] = tva
    return (label,images)




def fc_layer():
    # 命名空间
    with tf.name_scope('input'):
        # 这里的none表示第一个维度可以是任意的长度
        x = tf.placeholder(tf.float32, [1, 784], name='x-input')
        # 正确的标签
        y = tf.placeholder(tf.float32, [1, 10], name='y-input')

    keep_prob = tf.placeholder(tf.float32)
    lr = tf.Variable(0.001, dtype=tf.float32)

    # 显示图片
    with tf.name_scope('input_reshape'):
        image_shaped_input = tf.reshape(x, [-1, 28, 28, 1])
        tf.summary.image('input', image_shaped_input, 10)

    with tf.name_scope('layer1'):
        # 创建一个简单神经网络
        with tf.name_scope('weights1'):
            W1 = tf.Variable(tf.truncated_normal([784, 500], stddev=0.1), name='W1')
        with tf.name_scope('biases1'):
            b1 = tf.Variable(tf.zeros([500]) + 0.1, name='b1')
        with tf.name_scope('wx_plus_b1'):
            wx_plus_b1 = tf.matmul(x, W1) + b1
        with tf.name_scope('tanh1'):
            L1 = tf.nn.tanh(wx_plus_b1)
        with tf.name_scope('dropout1'):
            L1_drop = tf.nn.dropout(L1, keep_prob)

    with tf.name_scope('layer2'):
        # 创建一个简单神经网络
        with tf.name_scope('weights2'):
            W2 = tf.Variable(tf.truncated_normal([500, 300], stddev=0.1), name='W2')
        with tf.name_scope('biases2'):
            b2 = tf.Variable(tf.zeros([300]) + 0.1, name='b2')
        with tf.name_scope('wx_plus_b2'):
            wx_plus_b2 = tf.matmul(L1_drop, W2) + b2
        with tf.name_scope('tanh2'):
            L2 = tf.nn.tanh(wx_plus_b2)
        with tf.name_scope('dropout2'):
            L2_drop = tf.nn.dropout(L2, keep_prob)

    with tf.name_scope('layer3'):
        # 创建一个简单神经网络
        with tf.name_scope('weights3'):
            W3 = tf.Variable(tf.truncated_normal([300, 10], stddev=0.1), name='W3')
        with tf.name_scope('biases3'):
            b3 = tf.Variable(tf.zeros([10]) + 0.1, name='b3')
        with tf.name_scope('wx_plus_b3'):
            wx_plus_b3 = tf.matmul(L2_drop, W3) + b3
    return wx_plus_b3,keep_prob,x,y;





def test(data_set):
    with tf.Graph().as_default():
        logits,keep_prob,x,y = fc_layer()
        saver = tf.train.Saver()
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver.restore(sess, "./../../datas/logs/share/mnist/fc/projector/projector/a_model.ckpt-10001")
            prediction = tf.argmax(logits, 1)
            predint = prediction.eval(feed_dict={
                x: data_set[1],
                y: data_set[0],
                keep_prob: 1.0
            }, session=sess)
            return predint[0]

def main():
    for root, dirs, files in os.walk('./../../datas/test/mnist'):
        for file in files:
            print(file,test(readData(os.path.join(root,file),file)))
if __name__ == '__main__':
    main()
