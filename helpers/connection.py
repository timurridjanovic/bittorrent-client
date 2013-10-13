import struct
import socket

MAX_BUFFER_SIZE = 4096

PEER_ID = '-HS0001-123456789027'
PSTRLEN = '\x13'
PSTR = 'BitTorrent protocol'
RESERVED = '\x00\x00\x00\x00\x00\x00\x00\x00'

class Connection(object):
    def __init__(self, peers_list):
        self.peers_list = peers_list
        self.handshake = None
        self.info_hash = None
        
    def get_handshake(self, info_hash):
        self.info_hash = info_hash
        self.handshake = "%s%s%s%s%s" %(PSTRLEN, PSTR, RESERVED, info_hash, PEER_ID)
        return self.handshake
        
    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('41.249.212.56', 15613)) #hardcoded values TODO: change this
        
        s.send(self.handshake) #sending handshake
        
        #handshake: <pstrlen><pstr><reserved><info_hash><peer_id>
        
        #receiving handshake back from the server
        received_handshake = s.recv(MAX_BUFFER_SIZE) #receiving first 8 bytes which represent the length of pstr
        #pstr = s.recv(pstrlen)
        
        #print pstrlen
        start_index = 0
        
        pstrlen = struct.unpack('B', received_handshake[0])[0]
        pstr = received_handshake[1:1+pstrlen]
        reserved = received_handshake[1+pstrlen:pstrlen+9] #next 8 bytes
        info_hash = received_handshake[pstrlen+9:pstrlen+9+20] #next 20 bytes
        peer_id = received_handshake[pstrlen+9+20:pstrlen+9+20+20] #next 20 bytes
        rest_of_message = received_handshake[pstrlen+9+20+20:] #rest of message
        
        
        if info_hash == self.info_hash:
            self.decode_message(rest_of_message)
        else:
            print "no match on info hash"
            s.close()
            
            
    def decode_message(self, rest_of_message):
        """
        messages: <length prefix><message ID><payload>
        """
        message_types = {
        -1: 'keep_alive',
        0: 'choke',
        1: 'unchoke',
        2: 'interested',
        3: 'not interested',
        4: 'have',
        # bitfield: Append <bitfield> later. Dynamic length.
        5: 'bitfield',
        6: 'request',
        # piece: Append <index><begin><block> later. Dynamic length.
        7: 'piece',
        8: 'cancel',
        9: 'port'
        }
    
        length = struct.unpack('>i', rest_of_message[0:4])[0]
        message_id = struct.unpack('B', rest_of_message[4:5])[0]
        payload = []
        
        for i in range(length):
            payload.append(struct.unpack('B', rest_of_message[5+i])[0])
        
        if message_types[message_id] == 'bitfield':
            self.handle_bitfield()
            print payload
        
    def handle_bitfield(self):
        pass
        
   
        
        
        
        
        

