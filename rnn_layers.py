from __future__ import print_function, division
from builtins import range
import numpy as np


"""
This file defines layer types that are commonly used for recurrent neural
networks.
"""


def rnn_step_forward(x, prev_h, Wx, Wh, b):
    """
    Run the forward pass for a single timestep of a vanilla RNN that uses a tanh
    activation function.

    The input data has dimension D, the hidden state has dimension H, and we use
    a minibatch size of N.

    Inputs:
    - x: Input data for this timestep, of shape (N, D).
    - prev_h: Hidden state from previous timestep, of shape (N, H)
    - Wx: Weight matrix for input-to-hidden connections, of shape (D, H)
    - Wh: Weight matrix for hidden-to-hidden connections, of shape (H, H)
    - b: Biases of shape (H,)

    Returns a tuple of:
    - next_h: Next hidden state, of shape (N, H)
    - cache: Tuple of values needed for the backward pass.
    """
    next_h, cache = None, None
    ##############################################################################
    # TODO: Implement a single forward step for the vanilla RNN. Store the next  #
    # hidden state and any values you need for the backward pass in the next_h   #
    # and cache variables respectively.                                          #
    ##############################################################################
    pass
    h=x.dot(Wx)+prev_h.dot(Wh)+b
    next_h=np.tanh(h)
    cache=x,Wx,prev_h,Wh,b,h,next_h
    ##############################################################################
    #                               END OF YOUR CODE                             #
    ##############################################################################
    return next_h, cache


def rnn_step_backward(dnext_h, cache):
    """
    Backward pass for a single timestep of a vanilla RNN.

    Inputs:
    - dnext_h: Gradient of loss with respect to next hidden state, of shape (N, H)
    - cache: Cache object from the forward pass

    Returns a tuple of:
    - dx: Gradients of input data, of shape (N, D)
    - dprev_h: Gradients of previous hidden state, of shape (N, H)
    - dWx: Gradients of input-to-hidden weights, of shape (D, H)
    - dWh: Gradients of hidden-to-hidden weights, of shape (H, H)
    - db: Gradients of bias vector, of shape (H,)
    """
    dx, dprev_h, dWx, dWh, db = None, None, None, None, None
    ##############################################################################
    # TODO: Implement the backward pass for a single step of a vanilla RNN.      #
    #                                                                            #
    # HINT: For the tanh function, you can compute the local derivative in terms #
    # of the output value from tanh.                                             #
    ##############################################################################
    pass
    x, Wx, prev_h, Wh, b, h, next_h=cache
    dh=dnext_h*(1-next_h**2)

    dWx=x.T.dot(dh)
    dx=dh.dot(Wx.T)
    dWh=prev_h.T.dot(dh)
    dprev_h=dh.dot(Wh.T)
    db=np.sum(dh,axis=0)
    ##############################################################################
    #                               END OF YOUR CODE                             #
    ##############################################################################
    return dx, dprev_h, dWx, dWh, db


def rnn_forward(x, h0, Wx, Wh, b):
    """
    Run a vanilla RNN forward on an entire sequence of data. We assume an input
    sequence composed of T vectors, each of dimension D. The RNN uses a hidden
    size of H, and we work over a minibatch containing N sequences. After running
    the RNN forward, we return the hidden states for all timesteps.

    Inputs:
    - x: Input data for the entire timeseries, of shape (N, T, D).
    - h0: Initial hidden state, of shape (N, H)
    - Wx: Weight matrix for input-to-hidden connections, of shape (D, H)
    - Wh: Weight matrix for hidden-to-hidden connections, of shape (H, H)
    - b: Biases of shape (H,)

    Returns a tuple of:
    - h: Hidden states for the entire timeseries, of shape (N, T, H).
    - cache: Values needed in the backward pass
    """
    h, cache = None, None
    ##############################################################################
    # TODO: Implement forward pass for a vanilla RNN running on a sequence of    #
    # input data. You should use the rnn_step_forward function that you defined  #
    # above. You can use a for loop to help compute the forward pass.            #
    ##############################################################################
    pass
    N,T,D=x.shape
    H=h0.shape[1]

    h=np.zeros((N,T,H))
    cache=list(np.zeros(T))
    '''
    h[:,0,:]=h0
    for i in range(T-1):
        h[:,i+1,:],cache[i]=rnn_step_forward(x[:,i+1,:],h[:,i,:],Wx,Wh,b)
    '''
    h[:,0,:],cache[0]=rnn_step_forward(x[:,0,:],h0,Wx,Wh,b)
    for i in range(T-1):
        h[:,i+1,:],cache[i+1]=rnn_step_forward(x[:,i+1,:],h[:,i,:],Wx,Wh,b)

    ##############################################################################
    #                               END OF YOUR CODE                             #
    ##############################################################################
    return h, cache


def rnn_backward(dh, cache):
    """
    Compute the backward pass for a vanilla RNN over an entire sequence of data.

    Inputs:
    - dh: Upstream gradients of all hidden states, of shape (N, T, H). 
    
    NOTE: 'dh' contains the upstream gradients produced by the 
    individual loss functions at each timestep, *not* the gradients
    being passed between timesteps (which you'll have to compute yourself
    by calling rnn_step_backward in a loop).

    Returns a tuple of:
    - dx: Gradient of inputs, of shape (N, T, D)
    - dh0: Gradient of initial hidden state, of shape (N, H)
    - dWx: Gradient of input-to-hidden weights, of shape (D, H)
    - dWh: Gradient of hidden-to-hidden weights, of shape (H, H)
    - db: Gradient of biases, of shape (H,)
    """
    dx, dh0, dWx, dWh, db = None, None, None, None, None
    ##############################################################################
    # TODO: Implement the backward pass for a vanilla RNN running an entire      #
    # sequence of data. You should use the rnn_step_backward function that you   #
    # defined above. You can use a for loop to help compute the backward pass.   #
    ##############################################################################
    pass

    N,T,H=dh.shape
    D=cache[0][0].shape[1]  #get D
    dx=np.zeros((N,T,D))
    dh0=np.zeros((N,H))

    #Frist we compute the derivative of the weight matrix w.r.t loss at each time step
    dWx_all=np.zeros((D,T,H))
    dWh_all=np.zeros((H,T,H))
    db_all=np.zeros((T,H))
    dprev_h=np.zeros((N,H))
    for i in range(T-1,0,-1):
        dx[:, i, :], dprev_h, dWx_all[:, i, :], dWh_all[:, i, :], db_all[i, :] = rnn_step_backward(dh[:, i, :]+dprev_h, cache[i])

    '''
        dx[:, i, :], dh0, dWx_all[:, i, :], dWh_all[:, i, :], db_all[i, :] = rnn_step_backward(
            dh[:, i, :], cache[i])
        dh[:,i-1,:]+=dh0
    '''
    '''
    for i in range(T-1):
        dx[:, -(i+1), :], dprev_h, dWx_all[:, -(i+1), :], dWh_all[:, -(i+1), :], db_all[-(i+1), :] = rnn_step_backward(
            dh[:, -(i+1), :]+dprev_h, cache[-(i+1)])
    '''

    dx[:,0,:],dh0,dWx_all[:,0,:], dWh_all[:,0,:], db_all[0,:]=rnn_step_backward(dh[:,0,:]+dprev_h,cache[0])
    dWx=np.sum(dWx_all,axis=1,keepdims=False)
    dWh=np.sum(dWh_all,axis=1,keepdims=False)
    db=np.sum(db_all,axis=0,keepdims=False)
    '''
    x, Wx, Wh, prev_h, next_h,_,_ = cache[-1]
    _, D = x.shape
    N, T, H = dh.shape
    dx = np.zeros((N, T, D))
    dh0 = np.zeros((N, H))
    dWx = np.zeros((D, H))
    dWh = np.zeros((H, H))
    db = np.zeros(H)
    dprev_h_ = np.zeros((N, H))
    for i in range(T - 1, -1, -1):
        dx_, dprev_h_, dWx_, dWh_, db_ = rnn_step_backward(dh[:, i, :] + dprev_h_, cache[i])
        dx[:, i, :] = dx_
        dh0 = dprev_h_
        dWx += dWx_
        dWh += dWh_
        db += db_
    '''
    ##############################################################################
    #                               END OF YOUR CODE                             #
    ##############################################################################
    return dx, dh0, dWx, dWh, db


def word_embedding_forward(x, W):
    """
    Forward pass for word embeddings. We operate on minibatches of size N where
    each sequence has length T. We assume a vocabulary of V words, assigning each
    word to a vector of dimension D.

    Inputs:
    - x: Integer array of shape (N, T) giving indices of words. Each element idx
      of x muxt be in the range 0 <= idx < V.
    - W: Weight matrix of shape (V, D) giving word vectors for all words.

    Returns a tuple of:
    - out: Array of shape (N, T, D) giving word vectors for all input words.
    - cache: Values needed for the backward pass
    """
    out, cache = None, None
    ##############################################################################
    # TODO: Implement the forward pass for word embeddings.                      #
    #                                                                            #
    # HINT: This can be done in one line using NumPy's array indexing.           #
    ##############################################################################
    pass
    out=W[x,:]
    cache=W,x
    ##############################################################################
    #                               END OF YOUR CODE                             #
    ##############################################################################
    return out, cache


def word_embedding_backward(dout, cache):
    """
    Backward pass for word embeddings. We cannot back-propagate into the words
    since they are integers, so we only return gradient for the word embedding
    matrix.

    HINT: Look up the function np.add.at

    Inputs:
    - dout: Upstream gradients of shape (N, T, D)
    - cache: Values from the forward pass

    Returns:
    - dW: Gradient of word embedding matrix, of shape (V, D).
    """
    dW = None
    ##############################################################################
    # TODO: Implement the backward pass for word embeddings.                     #
    #                                                                            #
    # Note that words can appear more than once in a sequence.                   #
    # HINT: Look up the function np.add.at                                       #
    ##############################################################################
    pass
    #N,T,D=dout.shape
    W,x=cache
    #out=W[x,:]
    #W.shape=(V,D),x.shape=(N,T),dout.shape=(N,T,D)
    dW=np.zeros_like(W)
    np.add.at(dW,x,dout)
    #dW[x] += dout # this will not work, see the doc of np.add.at其实实现的功能是一样的，但是这样就不行，怪哉！
    ##############################################################################
    #                               END OF YOUR CODE                             #
    ##############################################################################
    return dW


def sigmoid(x):
    """
    A numerically stable version of the logistic sigmoid function.
    """
    pos_mask = (x >= 0)
    neg_mask = (x < 0)
    z = np.zeros_like(x)
    z[pos_mask] = np.exp(-x[pos_mask])
    z[neg_mask] = np.exp(x[neg_mask])
    top = np.ones_like(x)
    top[neg_mask] = z[neg_mask]
    return top / (1 + z)


def lstm_step_forward(x, prev_h, prev_c, Wx, Wh, b):
    """
    Forward pass for a single timestep of an LSTM.

    The input data has dimension D, the hidden state has dimension H, and we use
    a minibatch size of N.

    Note that a sigmoid() function has already been provided for you in this file.

    Inputs:
    - x: Input data, of shape (N, D)
    - prev_h: Previous hidden state, of shape (N, H)
    - prev_c: previous cell state, of shape (N, H)
    - Wx: Input-to-hidden weights, of shape (D, 4H)
    - Wh: Hidden-to-hidden weights, of shape (H, 4H)
    - b: Biases, of shape (4H,)

    Returns a tuple of:
    - next_h: Next hidden state, of shape (N, H)
    - next_c: Next cell state, of shape (N, H)
    - cache: Tuple of values needed for backward pass.
    """
    next_h, next_c, cache = None, None, None
    #############################################################################
    # TODO: Implement the forward pass for a single timestep of an LSTM.        #
    # You may want to use the numerically stable sigmoid implementation above.  #
    #############################################################################
    pass
    a=x.dot(Wx)+prev_h.dot(Wh)+b
    a_i, a_f, a_o, a_g = np.split(a,4,axis=1)
    i = sigmoid(a_i)
    f = sigmoid(a_f)
    o = sigmoid(a_o)
    g = np.tanh(a_g)
    next_c = f*prev_c+i*g
    next_h = o*np.tanh(next_c)
    cache = x, prev_h, prev_c, Wx, Wh, a_i, a_f, a_o, a_g, b, i, f, o, g, next_h, next_c

    ##############################################################################
    #                               END OF YOUR CODE                             #
    ##############################################################################

    return next_h, next_c, cache


def lstm_step_backward(dnext_h, dnext_c, cache):
    """
    Backward pass for a single timestep of an LSTM.

    Inputs:
    - dnext_h: Gradients of next hidden state, of shape (N, H)
    - dnext_c: Gradients of next cell state, of shape (N, H)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient of input data, of shape (N, D)
    - dprev_h: Gradient of previous hidden state, of shape (N, H)
    - dprev_c: Gradient of previous cell state, of shape (N, H)
    - dWx: Gradient of input-to-hidden weights, of shape (D, 4H)
    - dWh: Gradient of hidden-to-hidden weights, of shape (H, 4H)
    - db: Gradient of biases, of shape (4H,)
    """
    dx, dprev_h, dprev_c, dWx, dWh, db = None, None, None, None, None, None
    #############################################################################
    # TODO: Implement the backward pass for a single timestep of an LSTM.       #
    #                                                                           #
    # HINT: For sigmoid and tanh you can compute local derivatives in terms of  #
    # the output value from the nonlinearity.                                   #
    #############################################################################

    x, prev_h, prev_c, Wx, Wh, a_i, a_f, a_o, a_g, b, i, f, o, g, next_h, next_c = cache
    # There are two paths for the gradients of terms w.r.t. dnext_c
    #  First compute the gradients of next_c (dnext_c) from the contribution of next_h (dnext_h)
    dnext_c_from_dnext_h = dnext_h*o*(1-(np.tanh(next_c))**2)
    # The total gradients w.r.t next_c is the sum of dnext_c and dnext_c_from_dnext_h
    dnext_c +=dnext_c_from_dnext_h
    # The rest are normal backward calculations
    dprev_c = dnext_c * f
    do = dnext_h * np.tanh(next_c)
    df = dnext_c * prev_c
    di = dnext_c*g
    dg = dnext_c*i
    da_g = dg * (1 - (np.tanh(a_g))**2)
    da_o = do * o * (1 - o)
    da_f = df * f * (1 - f)
    da_i = di * i * (1 - i)
    da = np.hstack((da_i,da_f,da_o,da_g))
    dx = da.dot(Wx.T)
    dWx = x.T.dot(da)
    dprev_h = da.dot(Wh.T)
    dWh = prev_h.T.dot(da)
    db = np.sum(da,axis=0)
    ##############################################################################
    #                               END OF YOUR CODE                             #
    ##############################################################################

    return dx, dprev_h, dprev_c, dWx, dWh, db


def lstm_forward(x, h0, Wx, Wh, b):
    """
    Forward pass for an LSTM over an entire sequence of data. We assume an input
    sequence composed of T vectors, each of dimension D. The LSTM uses a hidden
    size of H, and we work over a minibatch containing N sequences. After running
    the LSTM forward, we return the hidden states for all timesteps.

    Note that the initial cell state is passed as input, but the initial cell
    state is set to zero. Also note that the cell state is not returned; it is
    an internal variable to the LSTM and is not accessed from outside.

    Inputs:
    - x: Input data of shape (N, T, D)
    - h0: Initial hidden state of shape (N, H)
    - Wx: Weights for input-to-hidden connections, of shape (D, 4H)
    - Wh: Weights for hidden-to-hidden connections, of shape (H, 4H)
    - b: Biases of shape (4H,)

    Returns a tuple of:
    - h: Hidden states for all timesteps of all sequences, of shape (N, T, H)
    - cache: Values needed for the backward pass.
    """
    h, cache = None, None
    #############################################################################
    # TODO: Implement the forward pass for an LSTM over an entire timeseries.   #
    # You should use the lstm_step_forward function that you just defined.      #
    #############################################################################
    pass
    #lstm_step_forward(x, prev_h, prev_c, Wx, Wh, b)
    N,T,D=x.shape
    _,H=h0.shape
    prev_h=h0
    prev_c=np.zeros_like(h0)
    h=np.zeros((N,T,H))
    cache=list(np.zeros(T)) #This shoule be a list instead of a ndarray, because cache returned from each forward pass is a list
    for i in range(T):
        h[:,i,:],next_c,cache[i]=lstm_step_forward(x[:,i,:],prev_h,prev_c,Wx,Wh,b)
        prev_h,prev_c=h[:,i,:],next_c

    ##############################################################################
    #                               END OF YOUR CODE                             #
    ##############################################################################

    return h, cache


def lstm_backward(dh, cache):
    """
    Backward pass for an LSTM over an entire sequence of data.

    Inputs:
    - dh: Upstream gradients of hidden states, of shape (N, T, H)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient of input data of shape (N, T, D)
    - dh0: Gradient of initial hidden state of shape (N, H)
    - dWx: Gradient of input-to-hidden weight matrix of shape (D, 4H)
    - dWh: Gradient of hidden-to-hidden weight matrix of shape (H, 4H)
    - db: Gradient of biases, of shape (4H,)
    """
    dx, dh0, dWx, dWh, db = None, None, None, None, None
    #############################################################################
    # TODO: Implement the backward pass for an LSTM over an entire timeseries.  #
    # You should use the lstm_step_backward function that you just defined.     #
    #############################################################################
    pass
    N,T,H=dh.shape
    _,D=cache[0][0].shape
    dx=np.zeros((N,T,D))
    dh0=np.zeros((N,H))
    dWx=np.zeros((D,4*H))
    dWh=np.zeros((H,4*H))
    db=np.zeros((4*H))
    #lstm_step_backward(dnext_h, dnext_c, cache)
    dnext_c=np.zeros((N,H))   # Here just initiate dnext_c as zeros, cause the last term of c do not contribute to loss
    dprev_h=np.zeros((N,H))
    for i in range(T-1,-1,-1):
        dh_current=dh[:,i,:]+dprev_h  # At each time step, the gradients w.r.t. h[i] should add the terms passes from h[i+1]
        dx[:,i,:], dprev_h, dprev_c, dWx_temp, dWh_temp, db_temp = lstm_step_backward(dh_current,dnext_c,cache[i])
        dWx +=dWx_temp
        dWh +=dWh_temp
        db +=db_temp
        dnext_c =dprev_c
        dh0 =dprev_h

    ##############################################################################
    #                               END OF YOUR CODE                             #
    ##############################################################################

    return dx, dh0, dWx, dWh, db


def temporal_affine_forward(x, w, b):
    """
    Forward pass for a temporal affine layer. The input is a set of D-dimensional
    vectors arranged into a minibatch of N timeseries, each of length T. We use
    an affine function to transform each of those vectors into a new vector of
    dimension M.

    Inputs:
    - x: Input data of shape (N, T, D)
    - w: Weights of shape (D, M)
    - b: Biases of shape (M,)

    Returns a tuple of:
    - out: Output data of shape (N, T, M)
    - cache: Values needed for the backward pass
    """
    N, T, D = x.shape
    M = b.shape[0]
    out = x.reshape(N * T, D).dot(w).reshape(N, T, M) + b
    cache = x, w, b, out
    return out, cache


def temporal_affine_backward(dout, cache):
    """
    Backward pass for temporal affine layer.

    Input:
    - dout: Upstream gradients of shape (N, T, M)
    - cache: Values from forward pass

    Returns a tuple of:
    - dx: Gradient of input, of shape (N, T, D)
    - dw: Gradient of weights, of shape (D, M)
    - db: Gradient of biases, of shape (M,)
    """
    x, w, b, out = cache
    N, T, D = x.shape
    M = b.shape[0]

    dx = dout.reshape(N * T, M).dot(w.T).reshape(N, T, D)
    dw = dout.reshape(N * T, M).T.dot(x.reshape(N * T, D)).T
    db = dout.sum(axis=(0, 1))

    return dx, dw, db


def temporal_softmax_loss(x, y, mask, verbose=False):
    """
    A temporal version of softmax loss for use in RNNs. We assume that we are
    making predictions over a vocabulary of size V for each timestep of a
    timeseries of length T, over a minibatch of size N. The input x gives scores
    for all vocabulary elements at all timesteps, and y gives the indices of the
    ground-truth element at each timestep. We use a cross-entropy loss at each
    timestep, summing the loss over all timesteps and averaging across the
    minibatch.

    As an additional complication, we may want to ignore the model output at some
    timesteps, since sequences of different length may have been combined into a
    minibatch and padded with NULL tokens. The optional mask argument tells us
    which elements should contribute to the loss.

    Inputs:
    - x: Input scores, of shape (N, T, V)
    - y: Ground-truth indices, of shape (N, T) where each element is in the range
         0 <= y[i, t] < V
    - mask: Boolean array of shape (N, T) where mask[i, t] tells whether or not
      the scores at x[i, t] should contribute to the loss.

    Returns a tuple of:
    - loss: Scalar giving loss
    - dx: Gradient of loss with respect to scores x.
    """

    N, T, V = x.shape

    x_flat = x.reshape(N * T, V)
    y_flat = y.reshape(N * T)
    mask_flat = mask.reshape(N * T)

    probs = np.exp(x_flat - np.max(x_flat, axis=1, keepdims=True))
    probs /= np.sum(probs, axis=1, keepdims=True)
    loss = -np.sum(mask_flat * np.log(probs[np.arange(N * T), y_flat])) / N
    dx_flat = probs.copy()
    dx_flat[np.arange(N * T), y_flat] -= 1
    dx_flat /= N
    dx_flat *= mask_flat[:, None]

    if verbose: print('dx_flat: ', dx_flat.shape)

    dx = dx_flat.reshape(N, T, V)

    return loss, dx
