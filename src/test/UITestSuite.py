from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import time
import unittest

geckodriver_path = "/usr/local/bin/geckodriver"
service = Service(executable_path=geckodriver_path, log_path="/dev/null")
service.log_level = "fatal"

# Use the Service object when creating the Firefox WebDriver
driver = webdriver.Firefox(service=service)

driver.get("http://127.0.0.1:5000/")

start_input = driver.find_element(By.ID, "start")
start_input.send_keys("Brandywine Apartments, Brandywine, Amherst, MA, USA")
current_value = start_input.get_attribute("value")
assert current_value == "Brandywine Apartments, Brandywine, Amherst, MA, USA"

end_input = driver.find_element(By.ID, "end")
end_input.send_keys("Boulders Drive, Amherst, MA, USA")
current_value = end_input.get_attribute("value")
assert current_value == "Boulders Drive, Amherst, MA, USA"

percent_element = driver.find_element(By.ID, "percent")
percent_element.send_keys("150") 

# Retrieve the current value of the input element
current_value = percent_element.get_attribute("value")
assert current_value == "150"

select_element = driver.find_element(By.ID, "elevation")
select = Select(select_element)
select.select_by_value("max")
assert select.first_selected_option.text == "Maximum"

select_element = driver.find_element(By.ID, "algorithm")
select = Select(select_element)
select.select_by_value("dijkstra")
assert select.first_selected_option.text == "Dijkstra"

go_button = driver.find_element(By.ID, "go")
go_button.click()
time.sleep(5)

map_element = driver.find_element(By.ID, "map")
assert map_element.is_displayed(), "Map not created"
time.sleep(2)

reset_button = driver.find_element(By.ID, "reset")
reset_button.click()
time.sleep(1)

map_element = driver.find_element(By.ID, "map")
assert not map_element.is_displayed(), "Map not created"

stats_element = driver.find_element(By.ID, "statistics")

driver.quit()
