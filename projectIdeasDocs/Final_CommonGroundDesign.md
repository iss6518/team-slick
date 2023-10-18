Team Slick has decided to create CommonGround, a platform that connects people with shared interests and goals,
and acts as a mentorship, hobby-sharing, or partner-matching tool. 
--
This application allows individuals to match to another like-minded artist, engineer, foodie, or fanatic of any kind. 
Users can decide to sign up for mutual mentorship, collaboration, or a simple hang-out session based on a few of their top interests. 
For example, if a guitarist was looking to perform at a coffee shop and wanted a singer, they’d be matched with just that on CommonGround. 
Another use case would be if a new NYC resident was looking to find the best restaurants in their area, they’d find a foodie interested in joining them. 
Finally, if someone knew Web Development very well, and was looking to learn Mobile Development in exchange for teaching their own skillset- 
they’d find a mentee and mentor on CommonGround! 
Our application is versatile and aims to be the best platform to match like-minded individuals in this deeply disconnected world. 
Come join us in building community at CommonGroud!


Documentation:

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
/UserCreate  (create account) 
Fill in all DB values necessary for each user account

/UserDelete (delete account)
Delete user and all info from records (DB)

/UserEdit (edit account)
Edit vital information about yourself in our records (DB)

/UsersManage
User can either accept or reject a partnership request
Reject (flag for MANAGE would be FALSE)
User removed from THAT USER ID’s match list
Accept (flag for MANAGE would be TRUE)
User added to THAT USER ID’s match list

/UsersMatch Get the users with the same preferences
Preferences of User1 & find User2 (or multiple) with those preferences
Must match preferences:
Virtual preference, or proximity preference, gender, age, etc;

/HobbiesGet
All hobbies on DB are showed as options for user to select

/HobbiesSet
All hobbies that user wants to match for are saved under their ID 

/MatchRemove
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


Hobbies:
Swimming
Running
Violin
Drums
Crocheting
Web3
Artificial Intelligence
Gardening
Car Enthusiasts
Sports
Foodie
Dancing

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


