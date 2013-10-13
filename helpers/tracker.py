import bencode
import struct
import urllib2

BLOCK_SIZE = 6


class Tracker(object):
    def __init__(self, url):
        self.url = url
        self.decoded_response = None
        self.peers = None
    
    def get_response(self):
        response = urllib2.urlopen(self.url).read()
        self.decoded_response = bencode.bdecode(response)
        return self.decoded_response


    def get_peers_list(self, response):
	    if self.is_binary(response):
		    peers_block_list = []
		    numberOfPeers = len(self.peers)/BLOCK_SIZE
		    index_start = 0
		    for byte in range(numberOfPeers):
			    peer_block = self.peers[index_start: index_start + BLOCK_SIZE]
			    index_start += BLOCK_SIZE
			    peers_block_list.append(peer_block)
		    return self.decode_peers_list(peers_block_list)		
	    else:
		    return self.peers


    def decode_peers_list(self, block_list):
	    peers_list = []
	    for block in block_list:
		    ip = block[0:4]
		    port = block[4:]

		    ip_address = []
		    port_address = []

		    ip_address.append(str(struct.unpack('B', ip[0])[0]))
		    ip_address.append(str(struct.unpack('B', ip[1])[0]))
		    ip_address.append(str(struct.unpack('B', ip[2])[0]))
		    ip_address.append(str(struct.unpack('B', ip[3])[0]))
		    ip_address = '.'.join(ip_address)

		    port_address.append(str(struct.unpack('B', port[0])[0]))
		    port_address.append(str(struct.unpack('B', port[1])[0]))
		    port_address = ''.join(port_address)
		
		    peers_list.append({'ip': ip_address, 'port': port_address})
	    return peers_list
		


    def is_binary(self, response):
	    self.peers = response['peers']
	    return not isinstance(self.peers, list)
	        



