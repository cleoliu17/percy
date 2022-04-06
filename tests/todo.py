from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread

from percy import percy_snapshot
from selenium import webdriver
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# start the example app in another thread
httpd = HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)
thread = Thread(target=httpd.serve_forever)
thread.setDaemon(True)
thread.start()

# launch firefox headless
chrome_options = Options()
browser = webdriver.Chrome(options=chrome_options)

# go to the example app
browser.get("http://localhost:8000")
browser.implicitly_wait(10)

# snapshot empty state
percy_snapshot(browser, "Empty Todo State")

# snapshot with a new todo
new_todo_input = browser.find_element_by_class_name("new-todo")
new_todo_input.send_keys("Try Percy3")
new_todo_input.send_keys(Keys.ENTER)
percy_snapshot(browser, "With a Todo")

# snapshot with a completed todo
todo_toggle = browser.find_element_by_class_name("toggle")
todo_toggle.click()
percy_snapshot(browser, "Completed Todo")

# clean up
browser.quit()
httpd.shutdown()
