YOUTUBE VIDEO - https://youtu.be/w3bNP1W4AQ8

README file - Description of how to use the website (several paragraphs):

CheckIn50 is a tool users can utilize to find others who are doing the same activities that you want to do, whether that be having a meal, working out, studying, or chilling out. To begin, users should navigate to the webpage, which can be accessed by running Flask on our project folder. Once on the webpage, users will see a welcome message, including instructions to click on either Register or Login on the side navigation bar. If a user has never used the website before, they should click register to make a profile, after which they will automatically be logged in using the credentials that they register with. On the Register page, users will be prompted to enter a username and password, as well as a re-entry of their password to confirm its accuracy. As noted on the page, the password has certain security requirements, including being at least eight characters long and containing at least one capital letter, one symbol, and one number. If these security requirements are not met, the user forgets to enter a username or password, or their password and confirmation do not match, a message will appear either alerting them that their password is insecure, that they forgot their username or password, or that the password and confirmation do not match, depending on the situation, and an account will not be created. However, if there are no errors, they should be able to see a table with the column headings of “activity”, "session type", “location", "start time", and "end time" as they've been loggen in. However, if they already have a CheckIn50 profile, users can simply log in by entering their previous credentials into the login page. They should also see this table if they have successfully logged in using the login page.

This main table, accessible through clicking the CheckIn50 logo or the home button on the sidebar, highlights all of the activities that the logged-in user has entered into CheckIn50 for that particular day. While it will initially be empty, especially immediately after an account is created, this can be changed by clicking on the Daily Form button on the left sidebar. This links to a form with four sections for each of the types of activities that CheckIn50 supports. Users can fill out the section for the type of activity that they want to enter into CheckIn50 - they can fill out up to three entries for each type of activity, and up to all four types of activities, at one time. Once they click submit, the activities they listed should appear in the main table, which they are redirected to. Users can also update their daily activities that they’ve entered by filling out this form again being mindful of updating the particular meal or session slot that they wish to edit. 

Beneath the Daily Form tab are several tabs related to each of the four types of activities. By clicking on each of these tabs, users can see a list of their friends who are taking part in those activities, as well as the time and location of their friends’ activities. This table will remain empty, though, until a user adds friends.

Most of CheckIn50’s functionality comes from engaging with friends, which can be done using the Friends tab. Friendships are not reciprocal in CheckIn50, meaning that when User A adds User B as a friend, User B appears in User A’s friends list, but User A does not appear in User B’s friends list. This allows users to have more control over who they want to see the schedules of in their activities tabs and who they want to let access their personal information. To add a friend (User B), User A would enter User B’s username into the add friends input box and click the adjacent button. This would send a request to User B, popping up in the friend requests table that is on the same page when they log in using their credentials. If User B would like User A to see their daily plans, they can select User A’s name from the drop-down menu underneath the friend requests table, and press the accept button. This would add User B’s name to User A’s friends table and increase User A’s friend count. However, if they would not like to give this permission to User A, User B can remove the friend request by selecting User A’s name from the same drop-down menu and clicking Remove. Through using this feature, CheckIn50 implements an additional level of privacy on the sensitive information, such as location and daily plans, of its users. Once User B accepts the request, any activities that User B enters will be categorized into the Meal Time, Chill Time, Exercise Time, and Study time tables on User A's account.

Finally, to log out of their account, users can click the Logout button, which will return them to the register/login page.
