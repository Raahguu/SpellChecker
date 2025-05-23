#This is a spellchecker program created by Joshua Finlayson SN: 10691485
#This was created for the first assignment of unit CSP1150.3
#Developent started 05/03/2025

#this is an inbuilt python module that allows for the generation of random numbers
import random
#this is an inbuilt python module that allows for the current time to be read
import time
#this is an inbuilt python module that allows for the calculating of differences between objects
import difflib

#possible sentences that could be used as questions in the test
global POSSIBLE_SENTENCES

POSSIBLE_SENTENCES = ["Python is named not after the snake, but after the comedy group 'Monty Python'.",
					  "This program was created for a university assignment in \"Programming Principles\".",
					  "It's a lot harder to come up with 20 sentences 10 words in length then you would think.",
					  "What do black holes say when they collide? Nothing, they just waved.",
					  "Standing waves have a Crest, and a Trough; as well as Nodes and Anti-Nodes.",
					  "I need to come up with original sentences otheriwse I need to reference.",
					  "I was born the same year the original iPhone came out (2007).",
					  "Nmap is a very useful tool for port scanning.",
					  "Do you prefer to use Kali or Parrot? (These are linux distros).",
					  "This sentence is 10 words long in three... two... one...",
					  "Good luck in the test, unless this is you're last one then well done.",
					  "This program was coded in Python 3.12 (64-bit).",
					  "If you want a harder gameplay experience then use STRICT mode.",
					  "If you use IDLE to run python programs, that's okay. But I will judge you.",
					  "ssh is done on port 22 by default; eduroam (the ECU wifi) blocks it.",
					  "Most of these sentences have been on the longer side of 10 words.",
					  "Github is a great website for version control: especially between multiple people.",
					  "Visual Studio (2022+) really needs to update its settings for python syntax highlighting.",
					  "All the variables of this project are in snake_case to follow Python style guides",
					  "Burp Suite, Wireshark, Nmap, Ncat, Hydra, and Hashcat are tools for PenTesting."]

#define functions
#This calculates the accuracy of the players input compared to the target string
def calculate_accuracy(target_sentence : str, user_input : str, strict: bool):
	#if the game is not in strict mode then we dont care about capitalisation, so just get rid of it
	if not strict:
		target_sentence = target_sentence.lower()
		user_input = user_input.lower()

	accuracy = difflib.SequenceMatcher(None, target_sentence, user_input).ratio() * 100

	return int(accuracy)

#This calculates the users typing speed by dividing the amount of words they wrote by the time it took to right them
#s = n/t
def calculate_wpm(user_input : str, time_taken : float, accuracy : int):
	number_of_words = len(user_input.split())
	wpm = number_of_words / (time_taken / 60) * accuracy / 100
	return int(wpm)


#this allows the game to keep going until the user says they want to quit
while True:
	#setting up variables that store all the different rounds stats 
	accuracies =[]
	player_wpms = []

	print("Welcome to Joshua's Typing Test")

	#Get number of rounds for the test and validate said input
	while True:
		try:
			number_of_rounds = input(f"How many rounds do you want the game to be (must be between 3 and {len(POSSIBLE_SENTENCES)}): ")
			if not number_of_rounds.isdigit(): 1/0
			#if they didn't input anything
			if not number_of_rounds.strip():
				number_of_rounds = len(POSSIBLE_SENTENCES)
			number_of_rounds = int(number_of_rounds)
			#if the number is within the correct bounds
			if number_of_rounds >= 3 and number_of_rounds <= len(POSSIBLE_SENTENCES):
				break
			#throw an error if they didnt pass either of the conditions above
			1/0
		except:
			print(f"Please enter an integer between 3 and {len(POSSIBLE_SENTENCES)}")

	#Do they want strict mode and validate that input
	print("Strict Mode means that your answers are case sensitive")
	#strict is false by default
	strict = False
	#loop until they provide a valid answer
	while True:
		strict_mode_str = input("Do you want to use strict mode (y/n): ").lower()
		#if they input they do want it, or did not input anything except whitespace
		if strict_mode_str == "y" or strict_mode_str == "yes" or not strict_mode_str.strip():
			strict = True
			break
		#If they inputed that they dont want strict mode
		if strict_mode_str == "n" or strict_mode_str =="no":
			break
		print("Please enter a 'y' or 'n' for yes or no respectively")

	#exposition info for the user on what choices they picked
	print(f"Your test will last {number_of_rounds} Rounds")
	if strict:
		print("And your input IS case sensitive")
	else: print("And your input is NOT case sensitive")
	print("If you want to finish early then just enter 'x' as an answer")

	#Deciding what sentences that the test will use and their order
	sentences_to_use = []
	unused_sentences : list = POSSIBLE_SENTENCES + [] #+ [] to ensure deep copy / value copy and not reference copy
	#loop through the number of questions and grab a random unchossen so far question
	for i in range(number_of_rounds):
		rand_int = random.randrange(0,len(unused_sentences))
		sentences_to_use.append(unused_sentences[rand_int])
		del unused_sentences[rand_int]
	
	input("Press Enter to begin: ")

	#The actual game code
	for i in range(0, number_of_rounds):
		#display teh round number and the question
		print(f"Round {i + 1}/{number_of_rounds}. Your sentence is: ")
		print(sentences_to_use[i])

		#get teh users input while timing them
		temp_time = time.time() * -1
		player_input = input()
		temp_time += time.time()

		#if they chose to skip the rest of the test
		if player_input.lower() == "x":
			break

		#calculate accuracy and words per minute of the player
		accuracies.append(calculate_accuracy(sentences_to_use[i], player_input, strict))
		player_wpms.append(calculate_wpm(player_input, temp_time, accuracies[-1]))

		#display results for this round to the player
		print(f"Accuracy: {accuracies[-1]:.0f}")
		print(f"WPM: {player_wpms[-1]:.0f}")
		input("Press enter to get the next question\n")
	
	#display the total results for the user
	print("You have completed the test.")
	print("Results: ")

	#if they skipped the whole game
	if len(accuracies) == 0:
		print("you don't have any results")
		print("you skipped the whole test")
		print("the WHOLE THING")
	#if they actually played the game
	else:
		#print accuracies
		print(f"Max Accuracy: {max(accuracies)}%")
		print(f"Average Accuracy: {sum(accuracies) / len(accuracies)}%")
		
		#print Words per Minute
		print(f"Max WPM: {max(player_wpms):.0f}")
		print(f"Average WPM: {sum(player_wpms) / len(player_wpms):.0f}")

		#print out a table for the results of every round
		print("Breakdown: ")
		print("Round \tAccuracy \tWPM")
		print("-"*5 + "\t" + "-" * 8 + "\t" + "-"*3)
		for i in range(0, len(accuracies)):
			print(f"{i+1} \t{accuracies[i]:.0f}% \t\t{player_wpms[i]:.0f}")
	
	#check if the player wants to retry the game
	inp = input("Would you like to play again (y/n): ").lower()
	#if they say no then end the game
	if inp == "n" or inp == "no":
		print("Goodbye then")
		print("Thanks for playing")
		input("Press enter to close the program\n")
		break
	#if they dont say no then reset the game