#!/usr/bin/env python3

import random

from network_rbf import RBFNetwork

# Number of listening nodes
NUM_LISTEN_NODES = 10000
# Number of non-listening nodes
NUM_PRIV_NODES = 50000
NUM_NODES = NUM_LISTEN_NODES + NUM_PRIV_NODES
# Number of networks to average over
NUM_NETWORKS = 10
# Number of random full-rbf pairs we draw to check whether there is a connection between them.
NUM_TRIES_PER_NETWORK = 100
# Number of extra preferential RBF connections per peer
NUM_EXTRA_RBF = 0

def main():
    # random.seed(12345)
    # p_rbf is the fraction of peers supporting full-RBF,
    # p_relay the probability that two of these nodes are connected
    print(f"p_rbf|p_relay")
    for p_rbf in [0.02, 0.04, 0.06, 0.08, 0.1, 0.12]:
        nRBF = int(p_rbf * NUM_NODES)
        nSuccess = 0
        for _ in range(NUM_NETWORKS):
            network = RBFNetwork(NUM_LISTEN_NODES, NUM_PRIV_NODES, nRBF, NUM_EXTRA_RBF)
            rbfListen = network.getRBFlisten()

            for _ in range(NUM_TRIES_PER_NETWORK):
                n1 = rbfListen[random.randint(0, len(rbfListen)-1)]
                n2 = rbfListen[random.randint(0, len(rbfListen)-1)]
                res = network.isConnectedViaRbf(n1, n2)
                nSuccess = nSuccess + res
        print(f"{p_rbf}|{nSuccess/(NUM_TRIES_PER_NETWORK * NUM_NETWORKS)}")


if __name__ == "__main__":
    main()
