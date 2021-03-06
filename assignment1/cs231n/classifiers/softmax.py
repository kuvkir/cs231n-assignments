from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange


def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    # (D,C)
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    # (N,C)

    #scores = X @ W
    #exp_scores = np.exp(scores)
    num_classes = W.shape[1]
    num_train = X.shape[0]
    loss = 0.0
    for i in range(num_train):
        scores = X[i] @ W
        correct_score = scores[y[i]]
        sumexp = 0
        for j in range(num_classes):
            sumexp += np.exp(scores[j])
        softmax = np.exp(correct_score) / sumexp
        loss -= np.log(softmax)

        for j in range(num_classes):
            if j == y[i]:
                dW[:, j] += (np.exp(correct_score) / sumexp - 1) * X[i]
            else:
                dW[:, j] += (np.exp(scores[j]) / sumexp) * X[i]

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    loss /= num_train
    loss += reg * np.sum(W * W)

    dW /= num_train
    dW += reg * 2 * W

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_classes = W.shape[1]
    num_train = X.shape[0]

    # (N,C)
    scores = X @ W
    # (N,1)
    correct_scores = scores[range(num_train), y].reshape(-1, 1)
    exp_correct_scores = np.exp(correct_scores).reshape(-1, 1)
    # (N,C)
    exp_scores = np.exp(scores)
    # (N,1)
    sumexp = np.sum(exp_scores, axis=1).reshape(-1, 1)
    # (N,1)
    softmax = exp_correct_scores / sumexp
    loss = -np.sum(np.log(softmax)) / num_train + reg * np.sum(W*W)

    m = np.zeros((num_train, num_classes))
    m[range(num_train), y] = 1
    dW = ((exp_scores / sumexp - m).T @ X).T / num_train + reg * 2 * W
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
