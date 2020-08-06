## Program runs and is up to date as of 8/6/2020. Instagram may change its front-end in the 
## future leading to bugs.

from selenium import webdriver
from secrets import username, password
from time import sleep

PATH = "C:\Program Files (x86)\Google\Chrome\chromedriver.exe"

class InstaBot:
	def __init__(self, username, password):
		self.driver = webdriver.Chrome(PATH)
		self.username = username ## Saving a reference to our username and password
		self.password = password ## incase we need it in other methods.
		
		
	def login_insta(self):
		self.driver.get("https://instagram.com") ## Opens up IG with the chrome driver.

		sleep(3) ## Wait for login page to load up.

		username_field = self.driver.find_element_by_xpath("//input[@name=\'username\']")\
			.send_keys(username)
		password_field = self.driver.find_element_by_xpath("//input[@name=\'password\']")\
			.send_keys(password)
		login_submit = self.driver.find_element_by_xpath("//button[@type='submit']")\
			.click()
		
		sleep(3) ## Waiting for the 'Do you want to save your login info' banner.

		dont_save_info = self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
			.click()

		sleep(3) ## Waiting for the 'Turn on notifications?' banner.

		disable_notifications = self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
			.click()

	def get_unfollowers(self):
		## Full XPath to profile page.
		self.driver.find_element_by_xpath("/html/body/div[1]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a")\
        	.click()
        
		sleep(3) ## Waiting for profile page to load. 

		## Full XPath to following list.
		self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")\
			.click()

		following = self.get_names() ## Associate a list of 'following' to the variable following

		## Full XPath to followers list.
		self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")\
        	.click()

		followers = self.get_names() ## Associate a list of 'followers' to the variable followers

		## List comprehension compares the 'following' list to the list of 'followers'.
		not_following_back = [user for user in following if user not in followers]

		print(not_following_back) 
		## A list of people who you follow but dont follow you back is generated in the terminal.

	def get_names(self):
		sleep(2) ## Waiting for followers/following list to load.

		scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]") ## Scroll box element.

		## On each scroll, we are comparing the height of the box currently to the height of the box previously.
		## If the height is the same, and we tried to scroll and we didn't get any more results, 
		## then we will stop. Within the while loop, we make last height as the current height and 
		## then we get a new height.

		last_ht, ht = 0, 1 

		while last_ht != ht:
			last_ht = ht
			sleep(1)

			## Javascript execution through Selenium. Scroll command.
			ht = self.driver.execute_script(
				"""
				arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
				""", scroll_box
				)
		links = scroll_box.find_elements_by_tag_name('a') ## Each name element is an anchor tag.
		
		## Retrieving the names of following/followers if the name is not blank.
		names = [name.text for name in links if name.text != ""]
		
		## Close button clicked.
		self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button")\
			.click()

		return names

## Main
my_bot = InstaBot(username, password)
my_bot.login_insta()
my_bot.get_unfollowers()