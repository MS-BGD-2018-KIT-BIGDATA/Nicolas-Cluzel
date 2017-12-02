import unittest
from collections import Counter
from collections import OrderedDict

# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    string2 = ''
    for i in range (0, n):
        string2 = string2 + string
    return string2



# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    #longueur=min(len(nums) & 4)
    for el in nums[:3]:
        if el == 9:
            return True
        
    return False

# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    if len(string) < 2:
        return 'Error, input string length must be at least 2.'
    count = 0
    for i in range (0, len(string) - 3):
        if string[i:i+2] == string[-2:]:
            count = count + 1
    return count    

#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):
    lengths = []
    for el in array:
        lengths.append(len(el))
    return lengths

#write fizbuzz programm
def fizbuzz(n):
    for x in range (0, n):
        if x % 3 == 0 and x % 5 != 0:
            print("Fizz")
        if x % 5 == 0 and x % 3 != 0:
            print("Buzz")
        if x % 3 == 0 and x % 5 == 0:
            print("FizzBuzz")
        if x % 3 != 0 and x % 5 != 0:
            print(x)

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    list=[]
    string = str(number)
    for i in range (0, len(string)):
        list.append(int(string[i]))
        
    return list

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
    word = ''
    result = ''
    l = []
    for w in text.split():
        word = w[1:] + w[0] + 'ay'
        l.append(word)
    result += l[0].capitalize() + ' '
    for i in range(1, len(l) - 1):
        result += l[i] + ' '
    result += l[len(l)-1]
    return result

#Write a proramm that returna dictionary of occurences of the alphabet for a given string.
# Test it with the Lorem upsuj
#"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
def occurences(text):
    #result = Counter(text.lower())
    result_letters = {}
    result = OrderedDict(sorted(Counter(text.lower()).items()))
    for k, v in result.items():
        if k.isalpha():
            result_letters[k] = v
            
        
    return result_letters

# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):
    fizbuzz(16)
    print (occurences("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."))
    def testArrayFront9(self):
        self.assertEqual(array_front9([1, 2, 9, 3, 4]) , True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]) , False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]) , False)

    def testStringTimes(self):
        self.assertEqual(string_times('Hel', 2),'HelHel' )
        self.assertEqual(string_times('Toto', 1),'Toto' )
        self.assertEqual(string_times('P', 4),'PPPP' )

    def testLast2(self):
        self.assertEqual(last2('hixxhi') , 1)
        self.assertEqual(last2('xaxxaxaxx') , 1)
        self.assertEqual(last2('axxxaaxx') , 2)

    def testLengthWord(self):
        self.assertEqual(length_words(['hello','toto']) , [5,4])
        self.assertEqual(length_words(['s','ss','59fk','flkj3']) , [1,2,4,5])

    def testNumber2Digits(self):
        self.assertEqual(number2digits(8849) , [8,8,4,9])
        self.assertEqual(number2digits(4985098) , [4,9,8,5,0,9,8])

    def testPigLatin(self):
        self.assertEqual(pigLatin("The quick brown fox") , "Hetay uickqay rownbay oxfay")

    

def main():
    unittest.main()

if __name__ == '__main__':
    main()
