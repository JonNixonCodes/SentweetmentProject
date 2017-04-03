import sentification_mod as sentification

s = sentification.Sentifier('TextBlob')
print (s.classifier_dict)
text = "Hello world, I'm so happy to finally be here, Yay!"
print(text)
print(s.sentiment(text))
print(s.subjectivity(text))
