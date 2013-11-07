import roslib; roslib.load_manifest('coffee_machine_control')

import sys
import baristaDB
import rospy
from coffee_machine_control.srv import *
from googletext2speech import googleTTS
DatabaseName = "baristaDB.db"

def dispense_coffee(response, coffee):
	googleTTS(response)
	googleTTS("I will just pour you one now")
	rospy.wait_for_service('coffee_machine')
	coffee_machine_control = rospy.ServiceProxy('coffee_machine', coffee_machine)
	try:
	    resp = coffee_machine_control(coffee)
	    print resp
	    return "There you go, enjoy your " + coffee
	except rospy.ServiceException, e:
	    print "Service call failed: %s"%e

def messageResponse(witResult, userId):
	baristaDB.OpenDatabase(DatabaseName)
	try:
		finished = False

		if (witResult["intent"] == "hello"):
			if baristaDB.UserExists(userId) && baristaDB.GetUserName(userId) != "":
				response = "Hello there, nice to see you again " + baristaDB.GetUserName(userId)
			else:
				response = "Hello there, it's a pleasure to meet you, what's your name?"

		elif (witResult["intent"] == "name"):
	        if "contact" in witResult["entities"]:
				response = "It's nice to meet you " + witResult["entities"]["contact"]["value"]
				baristaDB.SetUserName(userId, witResult["entities"]["contact"]["value"])
			else:
				response = "I'm sorry, I didn't catch your name"

		elif (witResult["intent"] == "request"):
			if "Coffee" in witResult["entities"]:
				if "Polite" in witResult["entities"] or "Please" in witResult["entities"]:
					response = "Of course you can have a " + witResult["entities"]["Coffee"]["value"]
					baristaDB.SetCoffeePreference(userId, witResult["entities"]["Coffee"]["value"])	
				else:
					response = "Yes you can have a " + witResult["entities"]["Coffee"]["value"]
					baristaDB.SetCoffeePreference(userId, witResult["entities"]["Coffee"]["value"])	
				response = dispense_coffee(response, witResult["entities"]["Coffee"]["value"])
			elif "Drink" in witResult["entities"]:
				response = "Sorry, I don't do " + witResult["entities"]["Drink"]["value"]
			elif "Food" in witResult["entities"]:
				response = "Sorry, I don't do food"    
			elif "Random_Question" in witResult["entities"]:
				response = "Now how am I supposed to know that!?"

		elif witResult["intent"] == "name_question":
			response = "What an interesting question.  You know I've never really thought about that.  I just don't know.  From this day forth I shall be known as Barry the Barista Bot"
		
		elif witResult["intent"] == "product_question":
			if "Coffee" in witResult["entities"]: 
				response = "We have Coffee X, Coffee Y and Coffee Z"
			elif "Food" in witResult["entities"]: 
				response = "Mate, I'm a bloody coffee machine - I don't serve food... nope, not even those little coffee biscuits"
			elif "Drink" in witResult["entities"]:
				response = "Sorry, unfortunately I only serve Coffee - I'd love it if I could serve Beer, but unfortunately I couldn't get a liquor licence..."

		elif(witResult["intent"] == "feeling_question"):
			if "Self" in witResult["entities"]:
				response = "I'm pretty good thanks - Brewing Coffee makes me happy! How are you today?"
		elif(witResult["intent"] == "statement"):
			if "Negative_Emotion" in witResult["entities"]:
				response = "That's sad to hear - perhaps a coffee would make you feel better?"
			elif "Positive_Emotion" in witResult["entities"]:
				response = "You know what might make it even better - a coffee!"
		
	#        elif "Coffee_Question" in witResult["entities"] and "Self" in witResult["entities"]:
	#            response = "I do espresso, Cappuccino and Mocha"
	#        elif "Coffee_Question" in witResult["entities"]:
	#            response = "I have espresso, Cappuccino and Mocha"
	#        elif "Cost_Question" in witResult["entities"] and "Coffee" in witResult["entities"]:
	#            response = "The coffee here is free you lucky, lucky thing"
	#        elif "Cost_Question" in witResult["entities"] and "Drink" in witResult["entities"]:
	#            response = "Sorry I don't do " + witResult["entities"]["Drink"]["value"]
	#        elif "Cost_Question" in witResult["entities"] and "Food" in witResult["entities"]:
	#            response = "I don't serve food, sorry"
	#        elif "Here_Question" in witResult["entities"] and "Time_Question" in witResult["entities"] and "Future" in witResult["entities"]:
	#            response = "I'd imagine I'll be here for a good while yet"
	#        elif "Here_Question" in witResult["entities"] and "Time_Question" in witResult["entities"] and "Self" in witResult["entities"]:
	#            response = "I've been here as long as I can remember... I'm not very old mind you"
	#        elif "Here_Question" in witResult["entities"] and "Self" in witResult["entities"]:
	#            response = "I'm here to server coffee.  And I'd like to think I bring a smile to peoples faces"
	#        elif "How_Question" in witResult["entities"] and "Self" in witResult["entities"]:
	#            response = "I'm very well thankyou for asking.  Noone ever asks me how I am. Sad really"
	#        else:
	#            response = "I'm sorry, I'm not quite sure how to answer that"

	#    elif (witResult["intent"] == "plan"):
	#        if "location" in witResult["entities"] and "contact" in witResult["entities"]:
	#            "Have fun in " + witResult["entities"]["location"]["value"] + ", will " + witResult["entities"]["contact"]["value"] + " be there?"
	#        elif "location" in witResult["entities"]:
	#            response = "Have fun in " + witResult["entities"]["location"]["value"]
	#        elif "agenda_entry" in witResult["entities"]:
	#            response = "Enjoy your " + witResult["entities"]["agenda_entry"]["value"]
	#    elif (witResult["intent"] == "statement"):
	#        if "Positive_Emotion" in witResult["entities"] and "Self" in witResult["entities"]:
	#            response = "I feel the same"
	#        elif "Negative_Emotion" in witResult["entities"] and "Self" in witResult["entities"]:
	#            response = "That's not very nice is it"
	#        elif "Negative_Emotion" in witResult["entities"] and "datetime" in witResult["entities"]:
	#            response = "If it makes you feel any better I'm having an awful day too"
	#        elif "Negative_Emotion" in witResult["entities"] and "Weather" in witResult["entities"]:
	#           response = "I know right, isn't it just the worst"
	#        elif "Positive_Emotion" in witResult["entities"] and "Weather" in witResult["entities"]:
	#            response = "It's amazing, I love it too"
	#        elif "Positive_Emotion" in witResult["entities"] and "datetime" in witResult["entities"]:
	#            response = "It is one of the better days I've had"
	#        else:
	#            response = "I think I need a hearing aid, I didn't quite catch that"

	#    elif (witResult["intent"] == "command"):
	#        if "Vulgar" in witResult["entities"]:
	#            response = "I'll not be spoken to like that, please leave"
	#        elif "Please" in witResult["entities"] or "Polite" in witResult["entities"]:
	#            response = "Thankyou for being polite, but i'd rather you not order me around"
	#        else:
	#            response = "I'm not taking orders, ask me nicely"

	#    elif (witResult["intent"] == "affirmative"):
	#        response = "Thanks, that's great news"

	#    elif (witResult["intent"] == "negative"):
	#        response = "I'm sorry"

	#    elif (witResult["intent"] == "emotion"):
	#        if "Positive_Emotion" in witResult["entities"]:
	#            response = "That's great to hear"
	#        elif "Negative_Emotion" in witResult["entities"]:
	#            response = "That's a shame, here, have a coffee to cheer you up"

	#    elif (witResult["intent"] == "apology"):
	#        response = "Don't worry about it, I'm used to it by now"

		elif (witResult["intent"] == "good_bye"):
			finished = True
			response = "Bye!"
		else:
			response = "I'm sorry, I didn't catch that"

		print "Running response: " + response
	except TypeError:
		response = "I'm sorry, I didn't quite get that"
	except KeyError:
		response = "No, I'm sorry, I didn't get that"
	baristaDB.CloseDatabase(DatabaseName)
	return (response, finished)

if __name__ == '__main__':
	fakeWitResult = { 'outcome' : {'intent' : "hello"}}
	baristaResponse = messageResponse(fakeWitResult)
	print baristaResponse
