from joker import Joker

j = Joker(None) 
j.addNode("localhost", "127.0.0.1", 22, "root", "password")
print j.discover() 
