#Einfuehrung in die Programmierung mit Python

'''
Eingabe und Ausgabe
'''

print 'hello, world!'
print 'hello, %s!' % ('world', )
print "hello, world!"

name = raw_input("What's your name? ")
print "hello, %s!" % (name, )

'''
Kontrollstrukturen

Wenn wir alle natürlichen Zahlen unter 10 auflisten, trifft das auf 3, 5 6 und 9 zu. Addiert ergeben die Zahlen 23.
Finde die Summe aller Vielfachen von 3 oder 5 unter 1000.

'''

sum = 0
for i in range(1000):
	if i % 3 == 0 or i % 5 == 0:
		sum += i
print "Die Summe beträgt %d" % (sum, )

'''
Max und Miggi laufen euporisch in Richtung Informatikraum, Max beginnt an Position 0 mit einer Geschwindigkeit von 4 LE/s, Miggi bewegt sich von Position 20 aus mit 2.5 LE/s. Nach wie vielen Sekunden überholt Max Miggi?
'''

max_pos = 0
max_vel = 4
miggi_pos = 20
miggi_vel = 2.5

t = 0
while max_pos < miggi_pos:
	max_pos += max_vel
	miggi_pos += miggi_vel
	t += 1
print 'Max holt Miggi nach %d Sekunden ein.' % (t, )


'''
Listen, Dictionarys, Tupel

Sortiere die Liste [3, 7, 8, 42, 5, 10] mit dem Selectionsort-Algorithmus!
'''

numbers = [3, 7, 8, 42, 5, 10]
sorted_list = []
while numbers:
	length = len(numbers)
	min_element = min(numbers)
	numbers.remove(min_element)
	sorted_list.append(min_element)
print "Die sortierte Liste lautet: ( %s )" % (sorted_list, )


'''
Schreibe ein Programm, dass die Wörter "house", "cat" und "black" ins Englische übersetzen kann.
Optional: Wenn der Benutzer ein anderes Wort eingibt, soll er die Möglichkeit haben, die Übersetzung in das Wörterbuch einzufügen.
'''

worldlist = {"house" : "Haus", "cat":"Katze", "black":"schwarz"}
inp = ""
while True:
	inp = raw_input("english word: ")
	if inp == '':
		break
	elif inp in worldlist.keys():
		translation = worldlist[inp]
		print 'The german term for "%s" is "%s"' % (inp, translation, )
	else:
		print 'Word not found!'
		translation = raw_input("What is the translation for %s? (leave blank to skip)" % (inp, ))
		worldlist[inp] = translation


'''
Funktionen

Gebe die Fibonnacci-Folge bis zu einem gegebenen Grenzwert aus
'''

def fib(limit, x=1, y=1):
	if y > limit:
		return ()
	return (x, ) + fib(limit, y, x+y)

if __name__ == '__main__':
	numbers = fib(100)
	print numbers
	print 'Die Fibonnacci-Folge bis 100:'
	print "\n".join([str(i) for i in numbers])
