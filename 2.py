import random
random.seed()
r=random.random() 
f = open( 'text.txt', 'w' )
for i in range(1,10001):
	f.write(str("%07i" %  i)+": "+str("%.9f" %  (random.random()))+"\n")
	# print (str("%04i" %  i))
f.close