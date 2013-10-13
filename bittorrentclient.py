import bencode
import os
import urllib2

from helpers.torrentfile import TorrentFile
from helpers.tracker import Tracker
from helpers.connection import Connection

filepath = '/home/timur/Downloads/'
filename = 'How to Start Working As a Freelance Web Designer.torrent'

def main():
    file = os.path.join(filepath, filename)
    
    torrentfile = TorrentFile(file) #get info from the tracker in the torrent file
    
    url = torrentfile.get_tracker_request_url() #create the get request url to send to the tracker server in order to get the tracker response
    
    info_hash = torrentfile.info_hash #get info hash for handshake

    tracker = Tracker(url) #create tracker object with the url (get request) passed as a parameter
    
    response = tracker.get_response() #send the get request to the tracker and store it in the response variable
    
    peers_list = tracker.get_peers_list(response) #decode the list of peers that are online (ips and ports).
    print peers_list
    
    connection = Connection(peers_list)
    
    handshake = connection.get_handshake(info_hash)
    
    connection.connect()
    
    
        
    
       

if __name__ == '__main__':
    main()
