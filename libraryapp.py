import sqlite3
import datetime
import random
conn = sqlite3.connect('library.db')

userID = input ("Please enter your ID: ")
dash = '-' * 115
def actionChoose():
	print("\n")
	print ("Choose from the following options: \n")
	print ("1. Find a book            2. Return item\n"+"3. Find an Event          4. Volunteer\n"+"5. Donate items           6. Request For Help\n" + "7. Exit")
	action = input("What would you like to do today? ")
	if action == '1':
		findBook()
	elif action == '2':
		returnItem()
	elif action == '3':
		findEvent()
	elif action == '4':
		volunteer()
	elif action == '5':
		donateItem()
	elif action == '6':
		requestLibarian()
	elif action == '7':
		print("Goodbye!")
	else:
		print("Please enter a valid action")
		action = input("What would you like to do today? ")
		actionChoose(action)

def findBook():
	count = 1
	bookTitle = input("Enter book title:")
	bookQuery = "SELECT * FROM item WHERE title=:bookTitle"
	cur.execute(bookQuery,{"bookTitle":bookTitle})
	bookRows = cur.fetchall()
	if bookRows:
		print("Here's what I found: ")
		print(dash)
		print('{:<4}{:<10}{:<10}{:<10}{:<30}'.format("    ","Title","Author","Type","Number of Available Copies"))
		print(dash)
		for bookRow in bookRows:
			print('{:<4}{:<10}{:<10}{:<10}{:<30}'.format(count,bookRow[0],bookRow[1],bookRow[2],bookRow[3]))
			count+=1;
		print("\n")
		######## BORROWING A BOOK ########
		borrows = input ("Would you like to borrow a book from above? (Y/N) ")
		if borrows == 'Y':
			borrowsNum = int(input("Please enter the number beside the book title: "))
			borrowBookTitle = bookRows[borrowsNum-1][0]
			borrowAuthorName = bookRows[borrowsNum-1][1]
			borrowBookCount = bookRows[borrowsNum-1][3]
			cur.execute('SELECT * FROM Borrows WHERE ID=? AND title=? AND authorName=?',(userID,borrowBookTitle,borrowAuthorName))
			borrowExist = cur.fetchall()
			### CHECKING IF THE PERSON HAS BORROWED THE SAME BOOK BEFORE ###
			if borrowExist:
				print("You have already borrowed that item! return it before borrowing")
				actionChoose()
			### CHECKING TO MAKE SURE THE BOOK IS AVAILABLE ###
			if borrowBookCount <= 0:
				print("Sorry that item is not Available")
				actionChoose()
			### BORROW THE BOOK ###
			cur.execute('UPDATE item SET count =?  WHERE title =? AND authorName=?',(borrowBookCount-1,borrowBookTitle,borrowAuthorName))
			cur.execute('INSERT INTO Borrows(ID,title,authorName,Fine,dueDate) VALUES (?,?,?,?,?)',(userID,borrowBookTitle,borrowAuthorName,0,datetime.date.today()+datetime.timedelta(days=30)))
			print("You have borrowed " + borrowBookTitle + " by "+ borrowAuthorName)
		else:
			actionChoose()
	else:
		print("Sorry I couldn't find anything on that")
	actionChoose()

def returnItem():
	returnBookTitle = input("Enter the title of the item you would like to return: ")
	returnAuthorName = input("Enter the author of the item you would like to return: ")

	bookQuery = "SELECT count FROM item WHERE title=:returnBookTitle AND authorName=:returnAuthorName"
	cur.execute(bookQuery,{"returnBookTitle":returnBookTitle,"returnAuthorName":returnAuthorName})
	bookRows = cur.fetchone()

	borrowsQuery = "SELECT * FROM Borrows WHERE ID=:userID AND title=:returnBookTitle AND authorName=:returnAuthorName"
	cur.execute(borrowsQuery,{"userID":userID, "returnBookTitle":returnBookTitle,"returnAuthorName":returnAuthorName})
	borrowsRows = cur.fetchall()

	if borrowsRows:
		returnBookCount = bookRows[0]
		cur.execute('UPDATE item SET count =?  WHERE title =? AND authorName=?',(returnBookCount+1,returnBookTitle,returnAuthorName))
		cur.execute('DELETE FROM Borrows WHERE ID =? AND title =? AND authorName=?',(userID,returnBookTitle,returnAuthorName))
		print("You have returned " + returnBookTitle + " by "+ returnAuthorName)
	else:
		print("Sorry you have not borrowed that book")
	actionChoose()

def requestLibarian():
	request = input ("What would you like to request? ")
	requestRows = True
	while requestRows:
		TicketNumber = random.randint(0,9999)
		cur.execute('SELECT requestID FROM requests WHERE requestID=?',(TicketNumber,))
		requestRows = cur.fetchall()
	cur.execute('INSERT INTO requests(requestID, ID) VALUES (?,?)', (TicketNumber, userID))
	cur.execute('INSERT INTO RequestsList(requestID, request) VALUES (?,?)', (TicketNumber, request))
	print("Your request has been processed")
	actionChoose()

def findEvent():
	count = 1
	eventName = input("Enter event name:")
	eventQuery = "SELECT * FROM Events WHERE eventName=:eventName"
	cur.execute(eventQuery,{"eventName":eventName})
	eventRows = cur.fetchall()
	if eventRows:
		print("Here's what I found: ")
		print(dash)
		print('{:<4}{:<25}{:<17}{:<25}{:<10}{:<15}{:<10}'.format("    ","Event Name","Event Type","Recommended Audience","Room #","Date","Location"))
		print(dash)
		for event in eventRows:
			print('{:<4}{:<25}{:<17}{:<25}{:<10}{:<15}{:<10}'.format(count,event[0],event[1],event[2],event[3],event[4],event[5]))
			count += 1
		print("\n")
		registers = input ("Would you like to register for an event from above? (Y/N) ")
		if registers == 'Y':
			registerNum = int(input("Please enter the number beside the event title: "))
			registerEventName = eventRows[registerNum-1][0]
			cur.execute('SELECT * FROM Registers WHERE ID =? AND eventName=?',(userID,registerEventName))
			registerExist = cur.fetchone()
			if registerExist:
				print("You have registered for this event already!")
				actionChoose()
			else:
				cur.execute('INSERT INTO Registers(ID,eventName) VALUES (?,?)',(userID,registerEventName))
			print("You have registered for "+registerEventName+"!")
		else:
			actionChoose()
	else:
		print("Sorry I couldn't find anything on that")
	actionChoose()

def volunteer():
	cur.execute('SELECT * FROM Personnel WHERE ID =?',(userID,))
	volunteerID = cur.fetchone()
	if volunteerID:
		print("You're already volunteering/working for our library!")
	else:
		volunteerLocation = input("Which location would you like to volunteer for? ")
		print("Thank you for volunteering for the library!")
		cur.execute('INSERT INTO Personnel(ID,firstName,lastName,role,Salary,Location) VALUES (?,?,?,?,?,?)',(userID,firstName,lastName,"Volunteer",0,volunteerLocation))
	actionChoose()


def donateItem():
	donateItemTitle = input("Enter title of item: ")
	donateItemAuthor = input("Enter author of item: ")
	donateItemType = input("Enter type of item:(book, magazine, CD, etc.) ")
	donateItemCount = input("How many are you donating? ")
	cur.execute('SELECT * FROM FutureItem WHERE title =? AND authorName =? AND itemType =?',(donateItemTitle,donateItemAuthor,donateItemType))
	donated = cur.fetchone()
	if donated:
		donationcount = donated[3]
		cur.execute('UPDATE FutureItem SET count =? WHERE title =? AND authorName=? AND itemType =?',(donationcount+donateItemCount,donateItemTitle,donateItemAuthor,donateItemType))
	else:
		cur.execute('INSERT INTO FutureItem(title,authorName, itemType, count, arrivalDate) VALUES (?,?,?,?,?)',(donateItemTitle,donateItemAuthor,donateItemType,donateItemCount,datetime.date.today()+datetime.timedelta(days=7)))
	print("Thank you for your donation!")
	actionChoose()

with conn:
    cur = conn.cursor()
    IDQuery = "SELECT * FROM Customer WHERE ID=:userID"
    cur.execute(IDQuery,{"userID":userID})
    rows=cur.fetchone()
    if rows:
    	firstName = rows[1]
    	lastName = rows[2]
    	print ("\n")
    	print ("++++++++++++++++++++++++++++++++++++++++++++++++")
    	print ("Welcome to the library "+firstName +" "+ lastName+"!")
    	actionChoose()
    else:
    	print("Sorry! your ID is not registered")
    
if conn:
	conn.commit()
	conn.close()
	print("Closed database successfully")