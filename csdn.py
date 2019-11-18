from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class csdn():
    def __init__(self):
        '''
        初始化，打开登录页面，等待登录
        '''
        options = webdriver.ChromeOptions()
        #设置默认下载路径，下载不弹窗
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': '/home/l/Downloads/csdn/'}
        options.add_experimental_option('prefs', prefs)
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 60, 1)
        

    def login(self):
        '''
        判断登录状态
        '''
        url = 'https://mp.csdn.net/'
        self.browser.get(url)
        print('wait login................')
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#sidebar > div:nth-child(4) > a.list-group-item.active' )))
        print('success login')

    def get_page_list(self):
        '''
        获取总页数，返回
        '''
        page_list_js = "return document.getElementsByClassName('page-link').length"
        pagell =  self.browser.execute_script(page_list_js)
        return pagell

    def get_article_list(self):
        '''
        获取当前页文章数量，返回
        '''
        article_list_length_js = "return document.getElementsByClassName('article-list-item-txt').length"
        articlell = self.browser.execute_script(article_list_length_js)
       
        print(articlell)
        return articlell

    def get_detail(self,item):
        '''
        新建文章编辑页面
        ''' 
        detail_js = f"document.getElementsByClassName('article-list-item-txt ')[{item}].getElementsByTagName('a')[0].click()"
        self.browser.execute_script(detail_js)
        

    def switch_window(self):
        '''
        切换到新建页面,
        等待导出btn
        导出为md，
        关闭当前页面，切回主页面
        '''
        handles = self.browser.window_handles
        print(handles)
        mhandle = handles[0]
        print(mhandle)
        newhandle = handles[1]
        print(newhandle)
        self.browser.switch_to.window(newhandle)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.app.app--light > div.layout > div.layout__panel.flex.flex--row > div.layout__panel.flex.flex--column > div.layout__panel.layout__panel--navigation-bar.clearfix > nav > div.scroll-box > div > div:nth-child(18) > button')))
        export_js = "return document.getElementsByClassName('navigation-bar__button button clearfix')[14].click();"
        self.browser.execute_script(export_js)
        epmd_js = "return document.getElementsByClassName('menu-entry button flex flex--row flex--align-center')[0].click();"
        self.browser.execute_script(epmd_js)
        time.sleep(1)
        self.browser.close()
        self.browser.switch_to.window(mhandle)


    def run(self):
        '''
        登录，
        获取总页数，
        获取每页文章数，
        进文章下载
        '''
        self.login()
        pagell =  self.get_page_list()
        for i in range(0,pagell):
            articlell = self.get_article_list()
            for i in range(0,articlell):
                self.get_detail(i)
                self.switch_window()

        print('success download')

if __name__ == "__main__":
    c = csdn()
    c.run()

    