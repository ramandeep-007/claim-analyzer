import string

n=input("Enter a claim:")
stop_words=['the','a','an','is','are','was','were','of','to','in','on','and']
clean_text="".join(char for char in n if char not in string.punctuation).lower().split()
clean_text=[i for i in clean_text if i not in stop_words]
print(clean_text)