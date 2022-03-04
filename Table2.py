from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as ec
PATH = './chromedriver'
driver = webdriver.Chrome(PATH)
driver.get("https://scholar.google.com/citations?view_op=view_org&org=10241031385301082500&hl=en&oi=io")
profile = []
df = pd.DataFrame({'title': [], 'authors': [], 'publication_date': [], 'description': [], 'cite_by': []})
authors = '-'
publication_date = '-'
description = '-'
cite_by = '-'
for i in range(30):
    for i in driver.find_elements(By.CSS_SELECTOR, "div.gs_ai_t"):
        a = i.find_element_by_css_selector('a')
        profile.append(a.get_attribute('href'))
    next_page = driver.find_element_by_css_selector(
        '#gsc_authors_bottom_pag > div > button.gs_btnPR.gs_in_ib.gs_btn_half.gs_btn_lsb.gs_btn_srt.gsc_pgn_pnx')
    next_page.click()

for user in profile:
    driver.get(user)
    while True:
        try:
            element = WebDriverWait(driver, 2).until(ec.element_to_be_clickable((By.ID, 'gsc_bpf_more')))
            element.click()
        except:
            break
    for i in driver.find_elements(By.CSS_SELECTOR, "tr.gsc_a_tr"):
        try:
            a = WebDriverWait(i, 2).until(ec.element_to_be_clickable((By.CSS_SELECTOR,'a')))
            a.click()
        except Exception:
            pass
        try:
            element = WebDriverWait(driver, 2).until(ec.presence_of_element_located((By.ID, 'gsc_ocd_view')))
        except:
            continue
        title = driver.find_element_by_id('gsc_vcd_title').text
        for j in driver.find_elements(By.ID, 'gsc_vcd_table'):
            authors = j.find_element_by_css_selector('#gsc_vcd_table > div:nth-child(1) > div.gsc_vcd_value').text
            try:
                publication_date = j.find_element_by_css_selector('#gsc_vcd_table > div:nth-child(2) > div.gsc_vcd_value').text
            except Exception:
                pass
            try:
                description = j.find_element_by_class_name('gsh_csp').text
            except Exception:
                pass
            try:
                 x = j.find_element_by_css_selector('#gsc_vcd_table > div:nth-child(9) > div.gsc_vcd_value > div:nth-child(1) > a').text
                 cite_by = x.split(' ')[-1]
            except Exception:
                pass

        df = df.append({'title': title, 'authors': authors, 'publication_date': publication_date,
                        'description': description, 'cite_by': cite_by}, ignore_index=True)
        driver.find_element_by_id('gs_md_cita-d-x').click()
        time.sleep(2)
df.to_csv("Papers Table.csv")
driver.quit()
