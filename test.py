students = ["amna", "emmy", "oriane", "gramond", "kristin"]


# student here can be anything
for student in students:
    print(student)

capitalized_students = []


for student in students:
    the_change = student.upper()
    capitalized_students.append(the_change)

capitalized_students = [student.upper() for student in students]

lower_tokens = [word.lower() for word in text1.tokens]

tokens = [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text)]

filename
raw_text
cleaned_text
sentences
tokenized sentences
tokens_without_sentences