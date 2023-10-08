CommonGround is a platform that connects people with shared interests and goals. It is a versatile application that acts as a mentorship, hobby sharing, or partner matching tool. 

Backend Implementation:

User Interface (for each user):
Login page (or create account)
Interest page (select all that apply)
Location page (with autolocate functionality?)
Preferences page (age, gender, virtual, proximity)
Matching page (with all available options, divided by activity)
Pending requests page (before other user accepts partnerships)
Manage requests page (where the user can accept/reject partnerships)
Matched page (where the user can see all accepted matches and their data)
Within each member, we have an option to chat & coordinate date/time
Utilize GCal Invitations, & Google Hangouts messaging (TBD)

API Endpoints:
EXTERNAL:
Google Maps API Call (/location)
Google Hangouts (/messaging) possibly SDK integration
Google Calendar (/invites) possibly SDK integration

INTERNAL:
/createUser  (create account) 
Fill in all DB values necessary for each user account


/deleteUser (delete account)
Delete user and all info from records (DB)

/editUser (edit account)
Edit vital information about yourself in our records (DB)


/getHobbies
All hobbies on DB are showed as options for user to select


/setHobbies
All hobbies that user wants to match for are saved under their ID 

/matchUsers Get the users with the same preferences
Preferences of User1 & find User2 (or multiple) with those preferences
Must match preferences:
Virtual preference, or proximity preference, gender, age, etc;


/manageUsers
User can either accept or reject a partnership request
Reject (flag for MANAGE would be FALSE)
User removed from THAT USER ID’s match list
Accept (flag for MANAGE would be TRUE)
User added to THAT USER ID’s match list


/removeMatch
For any reason that the user decides, they can redact a partnership by removing a match immediately
	

Database
Tables and Elements:
Users
Name
Age
Phone Number
Email
Primary Location
Interested Hobbies [array]


Hobbies 
Swimming
Running
Violin
Drums
Crocheting
Web3
Artificial Intelligence
Gardening
Car Enthusiasts

Locations
Pull from Google Maps API

Preferences
Gender
Age Range
Virtual/In Person
If in person, proximity preference


Flagged Users
Add with user Reporting and team evaluation


Matches
All user matches currently on platform

Data Protection:
All data will be encrypted
Another option would be that we save all data in a centralized database where the user accepts data usage for company
All terms and conditions would be clear (and can be revisited easily) for users

Outreach (Marketing)
Start with targeting clubs with similar interests at colleges in New York City
Blockchain Club, NYU <> Web3 Cohort, Columbia
Fashion Club, FIT <> Fashion & Design, Pace University
Running Club Baruch <> Running Club, Fordham

Business Outtake
VC funding
NYU Leslie ELab funding
Finance Details TBD


