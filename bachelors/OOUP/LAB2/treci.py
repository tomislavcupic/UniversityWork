def mymax(iterable, key=lambda x: x):
   max_x = max_key = None
   for x in iterable:
      if max_key is None or key(x) > max_key:
         max_x = x
         max_key = key(x)
   
   return max_x

def main():
   words = ["Gle", "malu", "vocku", "poslije", "kise", "Puna", "je", "kapi", "pa", "ih", "njise"]
   longest_word = mymax(words, key=lambda x: len(x))
   print("Najdulja riječ:", longest_word)

   D = {'burek': 8, 'buhtla': 5}
   most_expensive_product = mymax(D, key=D.get)
   print("Najskuplji proizvod:", most_expensive_product)

   people = [("John", "Doe"), ("Jane", "Smith"), ("Adam", "Johnson")]
   last_person = mymax(people)
   print("Posljednja osoba:", last_person)

   maxint = mymax([1, 2, 3, 4, 5])
   print("Najveći broj:", maxint)

   maxchar = mymax("Suncana strana ulice")
   print("Najveći znak:", maxchar)

   maxstring = mymax([ "Gle", "malu", "vocku", "poslije", "kise", "Puna", "je", "kapi", "pa", "ih", "njise"])
   print("Najveći string:", maxstring)

if __name__ == "__main__":
   main()