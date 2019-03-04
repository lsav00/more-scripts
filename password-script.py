#A password creation script that requires password meet specified requirements 

print("Passwords must be at least 8 characters long and have the following:")
print("-An uppercase letter,\n-A lowercase letter,\n-A number, and\n-A symbol.") 

count = 0   #Counts how many times password creation has been attempted

while (count < 4):  #"While loop" continues for four attempts
    score = 0       #Counter keeps "score" for how strong password is
    pw = input("Please enter a password: ")
    if len(pw) > 7: #"if" password length > 7, score increments
        score += 1
        
    for character in pw:        #for each character in the password...
        if character.isupper(): #if there's an uppercase letter...
            score += 1          #increment the score
            break               #break out of for loop when uppercase found
      
    for character in pw:        #for each character in the password...
        if character.islower(): #if there's a lowercase letter...
            score += 1          #increment the score
            break               #break out of for loop when lowercase found
        
    for character in pw:        #for each character in the password...
        if character.isnumeric():   #if there's a number...
            score += 1          #increment the score
            break               #break out of for loop when number found

    if not pw.isalnum():        #if the password is NOT solely alphanumeric...
        score +=1               #increment the score
        
    if score == 5:              #if score equals 5 (all conditions met)
        count = 5               #count becomes 5 and breaks out of loop
    else:                       #if conditions not met...
        print("Your password does not meet the listed requirements.")
        count +=1   #corresponding message displayed anc "count" incremented

#The below "if" statements are triggered when user leaves "while" loop                            
if count == 4:
    print("Too many tries!")
if count == 5:
    print("Password accepted!")
