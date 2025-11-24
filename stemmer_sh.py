import os
import collections
import re

class PunjabiStemmer:
    def __init__(self):
        # Define the base path relative to this script
        base_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        
        # Load the data files
        self.pronouns = self.load_words(os.path.join(base_path, 'Punjabi_Pronouns_sh.txt'))
        self.adverbs = self.load_words(os.path.join(base_path, 'Punjabi_Adverbs_sh.txt'))
        self.postpositions = self.load_words(os.path.join(base_path, 'Punjabi_Postpositions_sh.txt'))
        self.vocabulary = self.load_words(os.path.join(base_path, 'Punjabi_Vocabulary_sh.txt'))
        self.names = self.load_words(os.path.join(base_path, 'Punjabi_Boys_Girls_Names_sh.txt'))
        self.suffix = self.load_words(os.path.join(base_path, 'Suffix_sh.txt'))

        # In the development of the PunjabiStemmer, one of our core objectives was to create a highly accurate
        # and versatile tool capable of navigating the rich morphological landscape of the Punjabi language. To
        # achieve this, we have meticulously developed and implemented an expansive set of rules that serve as
        # the foundation of our stemming process.
        #
        # The PunjabiStemmer incorporates over 300 specific rules, designed to accurately process a wide array
        # of grammatical scenarios. These rules are meticulously categorized to address different aspects of the
        # language, including but not limited to, proper nouns and names, pronouns, verbs, adverbs, and adjectives.
        # This structured approach allows the stemmer to precisely identify and handle the morphological nuances
        # of Punjabi, significantly reducing errors related to overstemming and understemming.
        #
        # The rules are thoughtfully crafted and arranged from longest to smallest, optimizing both accuracy and
        # efficiency in stemming. This organization reflects our meticulous approach to handling the complexities
        # of Punjabi morphology.
        
        self.rules = [
{"match": "پوروک", "strip": "پوروک", "add": ""},
{"match": "اودیاں", "strip": "اودیاں", "add": ""},
{"match": "اندیاں", "strip": "اندیاں", "add": ""},
{"match": "ادیاں", "strip": "ادیاں", "add": ""},
{"match": "اونیاں", "strip": "اونیاں", "add": ""},
{"match": "ایا", "strip": "ایا", "add": ""},
{"match": "اون",  "strip": "ن", "add": ""},
{"match": "ٓون", "strip": "ون", "add": ""},
{"match": "اونی", "strip": "اونی", "add": ""},
{"match": "اوگڑا", "strip": "اوگڑا", "add": ""},
{"match": "کرن", "strip": "کرن", "add": ""},
{"match": "کارک", "strip": "کارک", "add": ""},
{"match": "جنک", "strip": "جنک", "add": ""},
{"match": "گردی", "strip": "گردی", "add": ""},
{"match": "تنتر", "strip": "تنتر", "add": ""},
{"match": "دائک", "strip": "دائک", "add": " "},
{"match": "دائیک", "strip": "دائیک", "add": " "},
{"match": "دارنی", "strip": "دارنی", "add": "دارنی"},
{"match": "نویس", "strip": "نویس", "add": " "},
{"match": "پرست", "strip": "پرست", "add": " "},
{"match": "پاتر", "strip": "پاتر", "add": " "},
{"match": "پورن", "strip": "'پورن", "add": " "},
{"match": "شکتی", "strip": "شکتی", "add": " "},
{"match": "شیلتا", "strip": "شیلتا", "add": " "},
{"match": "وانگیا", "strip": "وانگیا", "add": ""},
{"match": "اوانگا", "strip": "وانگا", "add": ""},
{"match": "اوانگی", "strip": "وانگی", "add": ""},
{"match": "اوانگے", "strip": "وانگے", "add": ""},
{"match": "یکرن", "strip": "یکرن", "add": " "},
{"match": " یکرن", "strip": " یکرن", "add": ""},
{"match": "وندا", "strip": "وندا", "add": ""},
{"match": "وندی", "strip": "وندی", "add": ""},
{"match": "وندے", "strip": "وندے", "add": ""},
{"match": "اونا", "strip": "اونا", "add": ""},
{"match": "اونی", "strip": "اونی", "add": ""},
{"match": "اونے", "strip": "اونے", "add": ""},
{"match": "اون", "strip": "اون", "add": ""},
{"match": "اوری", "strip": "اوری", "add": ""},
{"match": "ائی", "strip": "ائی", "add": ""},
{"match": "ਅਣ", "strip": "ਅਣ", "add": ""}, # in shahmukhi "ان" is part of words, and not just a suffix, e.g. "مہمان"; i am not transliterating to avoid potential issues ahead
{"match": "ਅਤ", "strip": "ਅਤ", "add": ""}, #same issue as "ان"
{"match": "آئی", "strip": "آئی", "add": ""},
{"match": "آو", "strip": "آو", "add": ""},
{"match": "آؤ", "strip": "آؤ", "add": ""},
{"match": "آؤں", "strip": "آؤں", "add": ""},
{"match": "آک", "strip": "آک", "add": ""},
{"match": "آنی", "strip": "آنی", "add": ""},
{"match": "آر", "strip": "آر", "add": ""},
{"match": "آرا", "strip": "آرا", "add": ""},
{"match": "آری", "strip": "آری", "add": ""},
{"match": "آل", "strip": "آل", "add": ""},
{"match": "آلا", "strip": "آلا", "add": ""},
{"match": "آلو", "strip": "آلو", "add": ""},
{"match": "ایل", "strip": "ایل", "add": ""},
{"match": "آڑی", "strip": "آڑی", "add": ""},
{"match": "اک", "strip": "اک", "add": ""},
{"match": "ات", "strip": "ات", "add": ""},
{"match": "یاں", "strip": "یاں", "add": ""},
{"match": "یا", "strip": "یا", "add": ""}, #ਇਆ my corpus does not have diacritics so transliterating without them
{"match": "یاں", "strip": "اں", "add": ""},
{"match": "یاں", "strip": "یاں", "add": ""},
{"match": "یا", "strip": "ا", "add": ""},
{"match": "یا", "strip": "یا", "add": ""},
{"match": "یا", "strip": "ا", "add": ""},
{"match": "ین", "strip": "ین", "add": ""},
{"match": "یئے", "strip": "یئے", "add": ""},
{"match": "یٹا", "strip": "یٹا", "add": ""},
{"match": "یٹی", "strip": "یٹی", "add": ""},
{"match": "یرا", "strip": "یرا", "add": ""},
{"match": "یلی", "strip": "یلی", "add": ""},
{"match": "یلا", "strip": "یلا", "add": ""},
{"match": "یگا", "strip": "یگا", "add": ""},
{"match": "یگی", "strip": "یگی", "add": ""},
{"match": "کار", "strip": "کار", "add": ""},
{"match": "کاری", "strip": "کاری", "add": ""},
{"match": "کشی", "strip": "کشی", "add": ""},
{"match": "خوراں", "strip": "خوراں", "add": ""},
{"match": "خور", "strip": "خور", "add": ""},
{"match": "کھور", "strip": "کھور", "add": ""},
{"match": "خانہ", "strip": "خانہ", "add": ""},
{"match": "گار", "strip": "گار", "add": ""},
{"match": "گری", "strip": "گری", "add": ""},
{"match": "گیر", "strip": "گیر", "add": ""},
{"match": "گر", "strip": "گر", "add": "گر"},
{"match": "غر", "strip": "غر", "add": "غر"},
{"match": "گھر", "strip": "گھر", "add": ""},
{"match": "گھنی", "strip": "گھنی", "add": "گھنی"}, #جਿੰਘਣی
{"match": "گھات", "strip": "گھات", "add": ""},
{"match": "چاری", "strip": "چاری", "add": ""},
{"match": "تن", "strip": "ن", "add": ""},
{"match": "تر", "strip": "تر", "add": ""},
{"match": "تائی", "strip": "تائی", "add": ""},
{"match": "تیرا", "strip": "تیرا", "add": ""},
{"match": "دان", "strip": "دان", "add": ""},
{"match": "داری", "strip": "داری", "add": ""},
{"match": "دل", "strip": "دل", "add": ""},
{"match": "دیاں", "strip": "اں", "add": ""}, # ਕੈਦਿਆਂ
{"match": "دیاں", "strip": "دیاں", "add": ""},
{"match": "ندیا", "strip": "ندیا", "add": ""},
{"match": "دیا", "strip": "دیا", "add": ""},
{"match": "دیا", "strip": "ا", "add": ""},
{"match": "پر", "strip": "پر", "add": ""},
{"match": "پار", "strip": "پار", "add": ""},
{"match": "ਧاਰی", "strip": "ਧاਰی", "add": ""},
{"match": "کار", "strip": "کار", "add": ""},
{"match": "نیاں", "strip": "اں", "add": ""},
{"match": "نیاں", "strip": "یاں", "add": ""},
{"match": "نیاں", "strip": "نیاں", "add": ""},
{"match": "پن", "strip": "پن", "add": ""},
{"match": "پنا", "strip": "پنا", "add": ""},
{"match": "پنّا", "strip": "پنّا", "add": ""},
{"match": "پر", "strip": "پر", "add": "پر"},
{"match": "پوش", "strip": "پوش", "add": ""},
{"match": "پنتھی", "strip": "پنتھی", "add": ""},
{"match": "بازی", "strip": "بازی", "add": ""},
{"match": "بان", "strip": "بان", "add": ""},
{"match": "باج", "strip": "باج", "add": ""},
{"match": "بندھ", "strip": "بندھ", "add": ""},
{"match": "باز", "strip": "باز", "add": ""},
{"match": "مان", "strip": "مان", "add": ""},
{"match": "مار", "strip": "مار", "add": ""},
{"match": "مکھی", "strip": "مکھی", "add": ""},
{"match": "مندی", "strip": "مندی", "add": ""},
{"match": "مند", "strip": "مند", "add": ""},
{"match": "نگے", "strip": "نگے", "add": ""},
{"match": "نیاں", "strip": "نیاں", "add": ""},
{"match": "یوگ", "strip": "یوگ", "add": ""},
{"match": "وانگا", "strip": "وانگا", "add": ""},
{"match": "وانگے", "strip": "وانگے", "add": ""},
{"match": "وانگی", "strip": "وانگی", "add": ""},
{"match": "ووگے", "strip": "ووگے", "add": ""},
{"match": "ویگا", "strip": "ویگا", "add": ""},
{"match": "ویگی", "strip": "ویگی", "add": ""},
{"match": "ون", "strip": "ون", "add": ""},
{"match": "ور", "strip": "ور", "add": ""},
{"match": "واد", "strip": "واد", "add": ""},
{"match": "وان", "strip": "وان", "add": ""},
{"match": "والا", "strip": "والا", "add": ""},
{"match": "اولی", "strip": "اولی", "add": "اولی"},
{"match": "اونی", "strip": "اونی", "add": ""},
{"match": "ون", "strip": "ون", "add": ""},
{"match": "ونی", "strip": "ونی", "add": ""},
{"match": "اون", "strip": "ون", "add": ""},
{"match": "اونی", "strip": "ونی", "add": ""},
{"match": "اونی", "strip": "نی", "add": ""},
{"match": "وال", "strip": "وال", "add": ""},
{"match": "ونتی", "strip": "ونتی", "add": ""},
{"match": "ونت", "strip": "ونت", "add": ""},
{"match": "وند", "strip": "وند", "add": ""},
{"match": "شاہی", "strip": "ی", "add": ""},
{"match": "شیل", "strip": "شیل", "add": ""},
{"match": "ساج", "strip": "ساج", "add": ""},
{"match": "ساز", "strip": "ساز", "add": ""},
{"match": "سار", "strip": "سار", "add": ""},
{"match": "شالا", "strip": "شالا", "add": "شالا"}, # ਗوشالا if we don't remove or add same suffix then stemmmer will continue steming
                                                  # because input word is valid but now we are adding same suffix and converting it to stem word output 
                                                   # which is now stemmed valid output so no further stemming take place so
{"match": "سال", "strip": "سال", "add": ""},
{"match": "سال", "strip": "سال", "add": "سال"},
{"match": "ہاری", "strip": "ہاری", "add": ""},
{"match": "ہارا", "strip": "ہارا", "add": ""},
{"match": "ہار", "strip": "ہار", "add": ""},
{"match": "ہین", "strip": "ہین", "add": ""},
{"match": "ہن", "strip": "ہن", "add": ""},
{"match": "اہن", "strip": "اہن", "add": ""},
{"match": "یوں", "strip": "یوں", "add": "ا"},
{"match": "ਿਓਂ", "strip": "ਿਓਂ", "add": "ੇ"},
{"match": "یو", "strip": "و", "add": ""},
{"match": "یو", "strip": "یو", "add": "ی"},
{"match": "یو", "strip": "یو", "add": "ا"},
{"match": "ਿੳ", "strip": "ਿੳ", "add": "ی"},
{"match": "ਿੳ", "strip": "ਿੳ", "add": "ا"},
{"match": "و", "strip": "و", "add": ""},
{"match": "یاں", "strip": "اں", "add": ""},
{"match": "یاں", "strip": "اں", "add": ""},
{"match": "یاں", "strip": "یاں", "add": "ا"}, #ਜاਗਦਿਆਂ
{"match": "یاں", "strip": "اں", "add": ""},
{"match": "یاں", "strip": "یاں", "add": ""}, #ਮੰਗਿਆਂ
{"match": "یا", "strip": "ا", "add": ""},
{"match": "یا", "strip": "یا", "add": "ا"},
{"match": "واں", "strip": "واں", "add": ""},
{"match": "ؤاں", "strip": "ؤاں", "add": ""},
{"match": "ੋਆਂ", "strip": "ਆਂ", "add": ""},
{"match": "اں", "strip": "اں", "add": ""},# ਨਹੁੰਆਂ
{"match": "ا", "strip": "ا", "add": ""},
{"match": 'جے', "strip": 'جے', "add": ""},
{"match": 'ائی', "strip": 'ی', "add": ""}, #ਗਹਿਰاਈ
{"match": 'ائی', "strip": 'ائی', "add": ""},
{"match": 'ائی', "strip": 'ائی', "add": "ائی"}, #ਅجਥاਈ
{"match": " ائی", "strip": "ی", "add": ""},
{"match": " ائی", "strip": " ائی", "add": ""},
{"match": "یئے", "strip": "یئے", "add": "ی"},
{"match": "یئے", "strip": "یئے", "add": ""},
{"match": "یئے", "strip": "ئے", "add": ""},
{"match": "یئے", "strip": "ئے", "add": "ا"},# ਏਰیਏ , ਮیਡیਏ 
{"match": "یئے", "strip": "یئے", "add": ""}, #ਦੇਖیਏ
{"match": "یں", "strip": "یں", "add": ""},
{"match": "ی", "strip": "ی", "add": ""},
{"match": "یائی", "strip": "یائی", "add": "ا"}, #ਚੰਗਿਆਈ
{"match": "ے", "strip": "ਏ", "add": ""},
{"match": "کا", "strip": "کا", "add": ""},
{"match": "کی", "strip": "کی", "add": ""},
{"match": "ک", "strip": "ک", "add": ""},
{"match": "کے", "strip": "کے", "add": ""},
{"match": "کے", "strip": "ے", "add": "ا"},
{"match": "کے", "strip": "کے", "add": "کے"}, #ਜاਣਕੇ , ਕਰਕੇ, ਮਿਲਕੇ,  ਕڑاਕੇ ,ਆਕੇ, ਬਣاਕੇ, ਬੰਨਕੇ
{"match": "یگی", "strip": "یگی", "add": ""},
{"match": "یگا", "strip": "یگا", "add": ""},
{"match": "وگی", "strip": "وگی", "add": ""},
{"match": "انگا", "strip": "انگا", "add": ""},
{"match": "انگی", "strip": "انگی", "add": ""},
{"match": "انگے", "strip": "انگے", "add": ""},
{"match": "وگی", "strip": "وگی", "add": ""},#ਕਰੋਗی
{"match": "وگی", "strip": "ی", "add": ""}, #ਯੋਗی
{"match": "گی", "strip": "گی", "add": ""},
{"match": "چی", "strip": "ی", "add": ""}, #جੋਚی
{"match": "چی", "strip": "چی", "add": "چی"}, #ਖਜاਨਚی
{"match": "انی", "strip": "انی", "add": "انی"},#سہارانی, پرانی پانی ڈھانی ہانی دھانی کہانی نوکرانی
{"match": "ونی", "strip": "ونی", "add": ""}, #جੈਣی
{"match": "ونی", "strip": "ونی", "add": "ونی"}, #ਧੂਣی
{"match": "نی", "strip": "ی", "add": ""}, #جੁਣی, ਚੁਣی, ਦੋਗੁਣی, ਨਿਗੁਣی, ਅਣجੁਣی, ਚੌਗੁਣی,
{"match": "نی", "strip": "نی", "add": ""},#ਭੁਗਤਣی, ਭੇਜਣی, ਪیਣی
{"match": "نی", "strip": "ی", "add": ""}, #ਬਣی
{"match": "نی", "strip": "نی", "add": "نی"}, #کاਣی ਗਿਣی
{"match": "انے", "strip": "ے", "add": "ے"}, #ਥاਣੇ ਗاਣੇ ਟਿکاਣੇ ਦاਣੇ
{"match": "ونے", "strip": "ے", "add": "ا"},
{"match": "ੁਣੇ", "strip": "ੇ", "add": ""},
{"match": "ینے", "strip": "ے", "add": "ا"},
{"match": "ੈਣੇ", "strip": "ੇ", "add": ""},
{"match": "نے", "strip": "ے", "add": "ا"}, # ਜاਣੇ, جاਮਣੇ,  ਲاਣੇ, ਛਣਕਣੇ
{"match": "ਣੇ", "strip": "ਣੇ", "add": ""}, #ਉਠਣੇ
{"match": "نا", "strip": "نا", "add": ""},
{"match": "ਣ", "strip": "ਣ", "add": ""},
{"match": "تی", "strip": "ی", "add": ""},
{"match": "تی", "strip": "تی", "add": "تی"},
{"match": "تا", "strip": "تا", "add": ""},
{"match": "ت", "strip": "ت", "add": ""},
{"match": "جی", "strip": "جی", "add": ""},
{"match": "ے", "strip": "ے", "add": "ا"},
{"match": "اندا", "strip": " ندا", "add": "ا"},
{"match": "اندی", "strip": "اندی", "add": "ا"},
{"match": " اندے", "strip": "  اندے", "add": "ا"},
{"match": "ندے", "strip": "ندے", "add": ""},
{"match": "ندی", "strip": "ندی", "add": ""},
{"match": "ندا", "strip": "ندا", "add": ""},
{"match": "ੰਦا", "strip": "ੰਦا", "add": ""},
{"match": "ੰਦی", "strip": "ੰਦی", "add": ""},
{"match": "ੰਦੇ", "strip": "ੰਦੇ", "add": ""},
{"match": "یدا", "strip": "یدا", "add": ""},
{"match": "دا", "strip": "دا", "add": ""},
{"match": "دی", "strip": "دی", "add": ""},
{"match": "دے", "strip": "دے", "add": ""},
{"match": "نی", "strip": "نی", "add": "نی"},
{"match": "نا", "strip": "نا", "add": ""},
{"match": "نے", "strip": "نے", "add": ""},
{"match": "ناں", "strip": "ناں", "add": ""},
{"match": "ن", "strip": "ن", "add": ""},
{"match": "پا", "strip": "پا", "add": ""},
{"match": "پ", "strip": "پ", "add": ""},
{"match": 'یلا', "strip": 'یلا', "add": ""},
{"match": " یلا", "strip": " یلا", "add": ""},
{"match": 'ولا', "strip": 'ولا', "add": ""},
{"match": " ੂਲا", "strip": " ੂਲا", "add": ""},
{"match": 'یلو', "strip": 'یلو', "add": ""},
{"match": "یل", "strip": "یل", "add": ""},
{"match": "لو", "strip": "لو", "add": ""},
{"match": "لا", "strip": "لا", "add": ""},
{"match": "ل", "strip": "ل", "add": ""},
{"match": "وی", "strip": "وی", "add": ""},
{"match": "واں", "strip": "واں", "add": ""},
{"match": "وا", "strip": "وا", "add": ""},
{"match": "و", "strip": "و", "add": ""},
{"match": "ویں", "strip": "ویں", "add": ""},
{"match": "ڑی", "strip": "ڑی", "add": ""},
{"match": "ڑا", "strip": "ڑا", "add": ""},
{"match": "ڑ", "strip": "ڑ", "add": ""},
{"match": "ج", "strip": "ج", "add": "ج"},
{"match": "ج", "strip": "ج", "add": ""},
{"match": " ا", "strip": " ا", "add": ""},
{"match": 'ا', "strip": 'ا', "add": ""},
{"match": "یں", "strip": "یں", "add": ""},
{"match": " ਿ", "strip": " ਿ", "add": ""},
{"match": "ی", "strip": "ی", "add": ""},
{"match": "ی", "strip":"ی", "add": "ی"},
{"match": 'ਿ', "strip": 'ਿ', "add": ""},
{"match": 'ی', "strip": 'ی', "add": ""},
{"match": 'و', "strip": 'و', "add": ""},
{"match": 'ੂ', "strip": 'ੂ', "add": ""},
{"match": " ੂ", "strip": " ੂ", "add": ""},
{"match": "اਂ", "strip": "اਂ", "add": ""},
{"match": "ੋ", "strip": "ੋ", "add": ""},
{"match": "وں", "strip": "وں", "add": ""},
{"match": "ੋ ਂ", "strip": "ੋ ਂ", "add": ""}
        ]
        self.dictionary_cache = {}
        self.rules_application_success = collections.defaultdict(int)
        self.rules_application_attempts = collections.defaultdict(int)
        

    def load_words(self, filename):
    # 
    # Loads words from a given file into a set. This method is primarily used
    # for loading lists of pronouns, adverbs, postpositions, vocabulary, names,
    # and suffixes from text files.
    
    # Parameters:
    # - filename (str): The path to the file containing the words.
    
    # Returns:
    # - set: A set of words loaded from the file.
    
    # If the file is not found, it returns an empty set and prints an error message.
    
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return set(line.strip() for line in file)
        except FileNotFoundError:
            print(f"Error: File not found {filename}")
            return set()

    def load_dictionary(self, char):
    
    # Loads a dictionary of words starting with a specific character from a file.
    # This method supports caching to avoid reloading the same dictionary multiple
    # times.
    
    # Parameters:
    # - char (str): The first character of the words to be loaded.
    
    # Returns:
    # - set: A set of words starting with the specified character.
    
        if char in self.dictionary_cache:
            return self.dictionary_cache[char]
        dictionary_path = os.path.join(os.path.dirname(__file__), '..', 'dictionaries', f"{char}.txt")
        try:
            with open(dictionary_path, "r", encoding="utf-8") as file:
                words = set(file.read().splitlines())
                self.dictionary_cache[char] = words
                return words
        except FileNotFoundError:
            return set()

    def is_valid_word(self, word):
    
    # Determines if a given word is valid by checking if it exists in the
    # dictionary loaded for its starting character.
    
    # Parameters:
    # - word (str): The word to check.
    
    # Returns:
    # - bool: True if the word is valid, False otherwise.
    
        if not word:
            return False
        first_char = word[0]
        dictionary = self.load_dictionary(first_char)
        is_valid = word in dictionary
        return is_valid

    def apply_rules(self, word):
    
    # Applies stemming rules to a given word. The rules are designed to handle
    # various grammatical structures in Punjabi, such as suffix stripping and
    # replacements, based on the morphological characteristics of the word.
    
    # Parameters:
    # - word (str): The word to be stemmed.
    
    # Returns:
    # - str: The stemmed word.
    
        for rule in self.rules:
            if word.endswith(rule["match"]):
                new_word = word[:-len(rule["strip"])] + rule["add"]
                if self.is_valid_word(new_word) or not self.is_valid_word(word):
                    return new_word
        return word

    def preprocess_text(self, text):
    
    # Cleans the input text by removing punctuation, special characters, and
    # emojis, while preserving Punjabi characters, numbers, and words from
    # other languages. Underscores are replaced with spaces to prevent word
    # merging.
    
    # Parameters:
    # - text (str): The text to be cleaned.
    
    # Returns:
    # - str: The cleaned text.
    
        text = text.replace('_', ' ')
        regex_pattern = r"[^\u0600-\u06FF0-9a-zA-Z\s]+"
        cleaned_text = re.sub(regex_pattern, '', text)
        return cleaned_text

    def stem_file(self, input_file_path, output_file_path):
    
    # Stems the content of a given input file and writes the stemmed text to an
    # output file. This method allows processing of larger texts or entire documents
    # stored in files.
    
    # Parameters:
    # - input_file_path (str): Path to the input file containing original text.
    # - output_file_path (str): Path where the stemmed text will be saved.
    
    
      try:
        # Open and read the input file
        with open(input_file_path, 'r', encoding='utf-8') as file:
            input_text = file.read()
        
        # Process (stem) the text
        stemmed_text = self.stem_text(input_text)
        
        # Write the stemmed text to the output file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(stemmed_text)
        
        print(f"Processed text has been saved to {output_file_path}")
      except FileNotFoundError:
        print(f"Error: The file {input_file_path} does not exist.")
      except Exception as e:
        print(f"An error occurred: {e}")

    def stem_word(self, word):
    
    # Stems a single word after preprocessing it to remove any noise. This
    # is a comprehensive method that combines cleaning and stemming for
    # individual words.
    
    # Parameters:
    # - word (str): The word to be stemmed.
    
    # Returns:
    # - str: The stemmed word.
    
        cleaned_word = self.preprocess_text(word)
        if cleaned_word in self.pronouns or cleaned_word in self.adverbs or cleaned_word in self.postpositions or cleaned_word in self.vocabulary or cleaned_word in self.names or cleaned_word in self.suffix:
            return cleaned_word
        return self.apply_rules(cleaned_word)

    def stem_text(self, text):
    
    # Stems a body of text, such as sentences or paragraphs, after preprocessing
    # to remove noise. This method is suitable for text analysis and processing
    # tasks that require stemming of multiple words in context.
    
    # Parameters:
    # - text (str): The text to be stemmed.
    
    # Returns:
    # - str: The stemmed text.
    
        cleaned_text = self.preprocess_text(text)
        words = cleaned_text.split()
        stemmed_words = [self.stem_word(word) for word in words]
        return ' '.join(stemmed_words)

# Add your stemming rules in the `self.rules` list as needed.
