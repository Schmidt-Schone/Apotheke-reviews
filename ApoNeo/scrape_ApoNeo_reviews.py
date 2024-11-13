from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.edge.service import Service as EdgeService  
from selenium.webdriver.edge.options import Options as EdgeOptions  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from webdriver_manager.microsoft import EdgeChromiumDriverManager  
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException  
import time  
  
def setup_driver():  
    edge_options = EdgeOptions()  
    edge_options.add_argument('--ignore-certificate-errors')  
    edge_options.add_argument('--ignore-ssl-errors')  
    service = EdgeService(EdgeChromiumDriverManager().install())  
    return webdriver.Edge(service=service, options=edge_options)  
  
def is_element_present(driver, selector):  
    try:  
        driver.find_element(*selector)  
        return True  
    except NoSuchElementException:  
        return False 

def click_star_icon(driver):
    try:
        # Locate the span element with class 'apn-icon active'
        star_icon_selector = (By.CSS_SELECTOR, "span.apn-icon.active")
        
        # Check if the element is present before clicking
        if is_element_present(driver, star_icon_selector):
            # Wait until the element is clickable
            star_icon = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(star_icon_selector)
            )
            
            # Scroll into view (if necessary) and click the element
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", star_icon)
            star_icon.click()
            print("Star icon clicked.")
        else:
            print("No reviews available")
            return
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Failed to click the star icon: {e}")
        print("No reviews available")     
  
def main():  
    driver = setup_driver()  
    try:  
        base_url = "https://www.aponeo.de/16538227-nurofen-junior-fieber-u-schmerzsaft-erdbe-40-mg-ml.html"  
        driver.get(base_url)
        time.sleep(30)

        #Main interaction
        click_star_icon(driver)
        time.sleep(60)

        html = driver.page_source  
        # save html to file in folder Reviews  
        with open("Reviews/ApoNeo.html", "w", encoding="utf-8") as f:  
            f.write(html)
  
    except Exception as e:  
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")  
    finally:  
        print("Schließe den Browser")  
        driver.quit()  
  
if __name__ == "__main__":  
    main()