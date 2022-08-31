#!/usr/bin/env python3

import random

NUM_FULL_OUTBOUND = 8
MAX_INBOUNDS = 115


class Network:
    nodes = []

    def __init__(self, nListen, nPrivate):
        self.nodes = []
        self.nListen = nListen
        self.nPrivate = nPrivate
        for i in range(nListen + nPrivate):
            self.nodes.append(Node())
        for i in range(nListen + nPrivate):
            self.addPeers(i)

    # TODO: Implement more peaked degree distributions - should be more realistic
    def addPeers(self, ownid):
        numOutbound = NUM_FULL_OUTBOUND
        out = 0
        while(out < numOutbound):
            peer = random.randint(0, self.nListen-1)
            if self.addConnection(ownid, peer) is True:
                out = out + 1

    def addConnection(self, ownid, peer):
            if (peer != ownid and len(self.nodes[peer].inbounds) < MAX_INBOUNDS and peer not in self.nodes[ownid].outbounds and peer not in self.nodes[ownid].inbounds):
                self.nodes[ownid].outbounds.add(peer)
                self.nodes[peer].inbounds.add(ownid)
                return True
            return False

class Node:
    def __init__(self):
        self.inbounds = set()
        self.outbounds = set()
        self.rbf = False
