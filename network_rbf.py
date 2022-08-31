#!/usr/bin/env python3

import random
from network import Network

class RBFNetwork(Network):
    def __init__(self, nListen, nPrivate, nRBF, extraRBFConn):
        super().__init__(nListen, nPrivate)
        self.extraRBFConn = extraRBFConn

        #Mark some peers as full-rbf supporting peers
        n = 0
        while(n < nRBF):
            node = random.randint(0, nListen + nPrivate - 1)
            if self.nodes[node].rbf is False:
                self.nodes[node].rbf = True
                n = n + 1

        # add preferential connections
        for i in range(nListen + nPrivate):
            self.addPreferentialPeers(i)

    def addPreferentialPeers(self, id):
        if self.nodes[id].rbf is False:
            return
        extrarbf = 0
        while(extrarbf  < self.extraRBFConn):
            peer = random.randint(0, self.nListen - 1)
            if self.nodes[peer].rbf is True and self.addConnection(id, peer) is True:
                extrarbf = extrarbf + 1

    def getRBFlisten(self):
        res = []
        for n in range(self.nListen):
            if self.nodes[n].rbf is True:
                res.append(n)
        return res

    # Check if two nodes are connected via full-RBF connections
    def isConnectedViaRbf(self, n1, n2):
        toProcess = set()
        visited = set()
        toProcess.add(n1)

        while(len(toProcess) > 0):
            curNode = toProcess.pop()
            if curNode == n2:
                return True
            if curNode not in visited:
                visited.add(curNode)
                for n in self.nodes[curNode].outbounds.union(self.nodes[curNode].inbounds):
                    if self.nodes[n].rbf == True and n not in visited:
                        toProcess.add(n)
        return False
