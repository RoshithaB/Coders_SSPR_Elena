from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import time
import unittest

# set the path to the gekodriver executable
geckodriver_path = "/usr/local/bin/geckodriver"
# create a service object for the gekodriver and configure logging
service = Service(executable_path=geckodriver_path, log_path="/dev/null")
service.log_level = "fatal"

# Use the Service object when creating the Firefox WebDriver
driver = webdriver.Firefox(service=service)

# open the specified URL in the firefox WebDriver
driver.get("http://127.0.0.1:5000/")

# find the input element with the 'ID "start" and enter the start location
start_input = driver.find_element(By.ID, "start")
start_input.send_keys("Brandywine Apartments, Brandywine, Amherst, MA, USA")
# Retrieve the current value of the start input element and assert that it matches the entered value
current_value = start_input.get_attribute("value")
assert current_value == "Brandywine Apartments, Brandywine, Amherst, MA, USA"

# Find the input element with the ID "end" and enter the location
end_input = driver.find_element(By.ID, "end")
end_input.send_keys("Boulders Drive, Amherst, MA, USA")
# Retrieve the current value of the end input element and assert that it matches the entered value
current_value = end_input.get_attribute("value")
assert current_value == "Boulders Drive, Amherst, MA, USA"

# Find the input element with ID "percent" and enter a value
percent_element = driver.find_element(By.ID, "percent")
percent_element.send_keys("150") 

# Retrieve the current value of the input element
current_value = percent_element.get_attribute("value")
assert current_value == "150"

# Find the select element with ID "elevation" and select the option with the value "max"
select_element = driver.find_element(By.ID, "elevation")
select = Select(select_element)
select.select_by_value("max")
assert select.first_selected_option.text == "Maximum"
# Find the select element with ID "algorithm" and select the option with the value "dijkstra"
select_element = driver.find_element(By.ID, "algorithm")
select = Select(select_element)
select.select_by_value("dijkstra")
assert select.first_selected_option.text == "Dijkstra"

# Find the button element with ID "go" and click it
go_button = driver.find_element(By.ID, "go")
go_button.click()
# Pause the execution for 5 seconds and allow the map to load
time.sleep(5)

# Find the map element with the ID "map" and assert that it is displayed
map_element = driver.find_element(By.ID, "map")
assert map_element.is_displayed(), "Map not created"
# Pause the execution for 2 seconds
time.sleep(2)

#Find the button element with ID "reset" and click it
reset_button = driver.find_element(By.ID, "reset")
reset_button.click()
# Pause the execution for 1 second
time.sleep(1)

# Find the element with ID "statistics" and retrieve its text
stats_element = driver.find_element(By.ID, "statistics")
statistics_text = stats_element.text
assert len(statistics_text) == 0

# Find the element with ID "directionsPanel" and retrieve its text
directions_element = driver.find_element(By.ID, "directionsPanel")
directions_text = directions_element.text
assert len(directions_text) == 0

# Quit the Firefox WebDriver, and closing the browser.
driver.quit()
