from bencode import bdecode, bencode
from urllib import urlencode
from hashlib import sha1

PEER_ID = '-HS0001-155367453324'


class TorrentFile(object):
    def __init__(self, filepath):
        f = open(filepath, 'rb') #read file in binary mode
        decoded_torrent_info = bdecode(f.read())
        
        self.title = decoded_torrent_info['title']
        self.announce = decoded_torrent_info['announce']

        self.info = decoded_torrent_info['info']
        self.filename = self.info['name']
        self.files = self.info['files']
        self.piece_length = self.info['piece length']
        self.pieces = self.info['pieces']
        self.info_hash = self.get_info_hash().digest()
       

    def get_info_hash(self):
        return sha1(bencode(self.info))

    def get_total_file_length(self):
        """
        go through all the files and add their length
        """
        file_length = 0

        for file in self.files:
            file_length += file.get('length', 0)
        
        return file_length


    def get_tracker_request_url(self):
        url_info = urlencode({
            'peer_id': PEER_ID,
            'info_hash': self.info_hash,
            'left': self.get_total_file_length()
        })
        
        return '?'.join([self.announce, url_info])
    

    def __str__(self):
        return 'title="%s"\nannounce="%s"\nfilename="%s"\npiece_length=%d\n' % (
            self.title, self.announce, self.filename, self.piece_length)

