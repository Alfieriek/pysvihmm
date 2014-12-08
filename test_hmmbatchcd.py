from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
import util
import hmmbatchcd as HMM

from scipy.spatial.distance import hamming as hd
from pybasicbayes.distributions import Gaussian
from util import *


def test_hmmbatchcd():
    """
    """

    K = 2
    D = 2
    kappa_0 = 1
    nu_0 = 4

    emit1 = Gaussian(mu=np.array([0,0]),
                     sigma=np.eye(2),
                     mu_0=np.zeros(2),
                     sigma_0=np.eye(2),
                     kappa_0=kappa_0,
                     nu_0=nu_0)
    emit2 = Gaussian(mu=np.array([5,5]),
                     sigma=np.eye(2),
                     mu_0=np.zeros(2),
                     sigma_0=np.eye(2),
                     kappa_0=kappa_0,
                     nu_0=nu_0)
    emit = np.array([emit1, emit2])

    N = 1000
    obs = np.array([emit[int(np.round(i/N))].rvs()[0]
                    for i in xrange(N)])
    
    mu_0 = np.zeros(D)
    sigma_0 = 0.75*np.cov(obs.T)
    kappa_0 = 0.01
    nu_0 = 4

    prior_emit = [Gaussian(mu_0=mu_0, sigma_0=sigma_0, kappa_0=kappa_0, 
                           nu_0=nu_0) for _ in xrange(K)]
    prior_emit = np.array(prior_emit)
    prior_tran = np.ones(K*K).reshape((K,K))
    prior_init = np.ones(K)

    hmm = HMM.VBHMM(obs, prior_init, prior_tran, prior_emit)
    hmm.infer()

    sts_true = np.array([int(np.round(i/N)) for i in xrange(N)])
    sts_pred = np.argmax(hmm.var_x, axis=1)
    match_perm = munkres_match(sts_true, sts_pred, K)
    sts_pred = match_perm[sts_pred]
    print 'Hamming Distance = ', hd(sts_pred, sts_true)

    plt.figure()
    plt.scatter(obs[:,0], obs[:,1])
    for G in prior_emit:
        plt.scatter(*G.mu_mf, color='green')
    for G in hmm.var_emit:
        plt.scatter(*G.mu_mf, color='red')
        util.plot_ellipse(G.mu_mf, G.sigma, edge='r', face='none')
    plt.show()

    
if __name__ == '__main__':
    test_hmmbatchcd()
