from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_class(CLASS_NAME, DEPT):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    main_page = "https://www.sis.itu.edu.tr/TR/ogrenci/ders-programi/ders-programi.php?seviye=LS"
    driver.get(main_page)
    sleep(1)
    driver.find_element_by_xpath("/html/body/div/div[2]/div/div[1]/form/div[2]/button/div/div").click()
    sleep(1)
    driver.find_element_by_xpath("/html/body/div/div[2]/div/div[1]/form/div[2]/div/div[1]/input").send_keys(CLASS_NAME[:3])
    sleep(0.3)
    driver.find_element_by_xpath("/html/body/div/div[2]/div/div[1]/form/div[2]/div/div[1]/input").send_keys(Keys.ENTER)
    sleep(0.3)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[1]/form/input").click()
    sleep(1)
    rows = []
    try:
        for i in range(1,100000):
            row = driver.find_element(By.XPATH,f"/html/body/div[1]/div[2]/div/div[3]/table/tbody/tr[{i}]")
            elements =[]
            for element in row.find_elements(By.TAG_NAME,"td"):
                elements.append(element.text)

            if i == 1:
                rows.append(elements)
            elif CLASS_NAME in elements or CLASS_NAME+"E" in elements:
                rows.append(elements)
    except Exception as e:
        print(e)
    driver.close()
    try:
        rows.pop(1)
    except:
        return None
    columns = rows.pop(0)
    df = pd.DataFrame(rows, columns=columns)
    #df[df["Kontenjan"].apply(lambda x: int(x))>0]
    df[df["Dersi Alabilen Programlar"].apply(lambda x: DEPT in x)]
    return df
if __name__ == "__main__":
    get_class()