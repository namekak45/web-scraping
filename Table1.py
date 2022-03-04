from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

PATH = './chromedriver'
driver = webdriver.Chrome(PATH)
driver.get("https://scholar.google.com/")
search_box = driver.find_element_by_css_selector("#gs_hdr_tsi")
search_box.send_keys("Thammasat University\n")
tu = driver.find_element_by_css_selector("#gs_res_ccl_mid > div:nth-child(2) > div > a")
tu.click()
df = pd.DataFrame(
    {
        'user_id': ['N5APA98AAAAJ'],
        'author': ['Wasit Limprasert'],
        'affiliation': ['Thammasat university']
    }
)
for i in range(30):
    for i in driver.find_elements(By.CSS_SELECTOR, "div.gs_ai_t"):
        a = i.find_element_by_css_selector('a')
        author = a.text
        user_id = a.get_attribute('href').split('=')[-1]
        affiliation = i.find_element_by_css_selector('div.gs_ai_aff').text
        df = df.append(
            {
                'user_id': user_id,
                'author': author,
                'affiliation': affiliation
            }, ignore_index=True
        )
    next_page = driver.find_element_by_css_selector('#gsc_authors_bottom_pag > div > button.gs_btnPR.gs_in_ib.gs_btn_half.gs_btn_lsb.gs_btn_srt.gsc_pgn_pnx')
    next_page.click()

df.to_csv("Authors Table.csv")
driver.quit()
