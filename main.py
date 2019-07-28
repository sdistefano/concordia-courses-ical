from selenium import webdriver
import time, yaml

driver = webdriver.Firefox()

credentials = yaml.load('credentials')

courses = []

def login():
    driver.get('https://my.concordia.ca/psp/upprpr9/?cmd=login&languageCd=ENG')
    driver.find_element_by_name('userid').send_keys(credentials['username'])
    driver.find_element_by_name('pwd').send_keys(credentials['password'])
    driver.find_element_by_class_name('form_button_submit').click()

def get_term_info(term):
    term.find_elements_by_tag_name('td')[0].find_element_by_tag_name('input').click()
    driver.find_element_by_id('DERIVED_SSS_SCT_SSR_PB_GO').click()
    time.sleep(2)
    _courses = driver.find_elements_by_class_name('PSGROUPBOXWBO')[1:]
    for course in _courses:
        c = {}
        c['name'] = course.find_element_by_class_name('PAGROUPDIVIDER').get_attribute('innerHTML')
        c['number'], c['section'], c['component'], c['times'], c['room'], c['instructor'], c['start_end'] =\
            map(lambda x: x.text,
                course.find_elements_by_tag_name('tr')[-1].find_elements_by_tag_name('td')
            )
        courses.append(c)

def get_courses():
    url = 'https://campus.concordia.ca/psc/pscsprd/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL?Page=SSR_SSENRL_LIST&Action=A&TargetFrameName=None'
    driver.get(url)
    gt = lambda: driver.find_element_by_css_selector('.PSLEVEL2GRID').find_elements_by_tag_name('tr')[1:]
    terms = gt()
    nterms = len(terms)
    while nterms:
        driver.get(url)
        terms = gt()
        get_term_info(terms[nterms-1])
        nterms -= 1
    0

def main():
    login()
    get_courses()

main()