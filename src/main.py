import string

n=input("Enter a claim:")
clean_text="".join(char for char in n if char not in string.punctuation).lower().split()
print(clean_text)