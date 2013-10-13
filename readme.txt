each client would need a 

-listening thread (TCP connection)
-sending thread (writes to the same peer)
-peers aknowledge what pieces to send
-requesting blocks (the piece size is a constant except for the last one which is the rest...)



Problems: when to send requests





-Connect to peer with handshake
-get handshake response, unpack handshake

pstrlen
pstr
reserved
info_hash (only thing that changes in the handshake)
peer_id



get first 4 bytes after handshake

Handshake
Messages
<length> <id>   <payload>
1 byte  1 byte  rest




