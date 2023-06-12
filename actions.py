from argparse import Action
import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import numpy
import re
import datetime

class SeleniumActions():
    def __init__(self,webdriver,waitor,vars) -> None:
        self.driver=webdriver
        self.waitor=waitor
        self.vars = vars
        self.vars["window_handles"] = self.driver.window_handles

    def wait_for_window(self, timeout= 2):
        time.sleep(round(timeout))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def get_locator_type(self,ele_loc_str):
        locating_type=""
        if ele_loc_str.strip().startswith("/"): #xpath
            locating_type=By.XPATH
        else:       # 除了 xpath 之外 都算作 css selector
            locating_type=By.CSS_SELECTOR
        return locating_type
        
        
    def wait_before_after(self,ele_loca_str):
        
        try:
            due=re.match(r"^(\d+)s$",ele_loca_str)
            if due:
                # self.driver.implicitly_wait(int(due.group(1)))
                self.wait_for_window(int(due.group(1)))
            else:
                locating_type=self.get_locator_type(ele_loca_str)
                self.waitor.until(lambda d: d.find_element(locating_type,ele_loca_str))
        except Exception as e:
            print(e)
    
    def get_value_with_variable(self,value):
        '''
        对值 的字符串 进行处理，如果值中有 预定义变量，则处理预定义变量后 再返回字符串
        预定义变量：
            $Cur_Day ： 返回当前日期字符串
        '''
        if '$Cur_Day' in value:
            curday_str=datetime.date.today().strftime("%Y%m%d")
            return value.replace('$Cur_Day',curday_str)
        else:
            return value


    def action_on_ele(self,action_type,ele_loc_str,value_on_ele):
        '''
         this function is used to act on browser
         action_type=[验证,访问,点击,双击,键盘输入,移动相对位移后-点击,移动相对位移后-点右键,点击-移动相对位移后-点击,点击-移动相对位移后-点右键,右键,移动到元素后点击,清除输入]
        '''   
        if action_type=='验证': # 如果是 验证，不作任何动作
            pass

        if action_type=='访问' and str(ele_loc_str)!=str(numpy.NaN):
            if str(value_on_ele)!=str(numpy.NaN) or str(value_on_ele)!=str(numpy.NaN):      ## 如果网址带有参数，value_on_ele 用于存储参数, 例如：?pageSize=50&pageNum=2
                self.driver.get(ele_loc_str.strip()+str(value_on_ele))
            else:
                self.driver.get(ele_loc_str.strip())        ## 网址不带参数

        if action_type=='点击' and str(ele_loc_str)!=str(numpy.NaN):
            if self.vars['found_element'] is None:      # 不是通过 “寻找” 这一环节来定位的
                locating_type = self.get_locator_type(ele_loc_str)
                self.waitor.until(lambda d: d.find_element(locating_type,ele_loc_str)).click()
            else:
                self.vars['found_element'].click()
                self.vars['found_element']=None
            
        if action_type=="双击":
            if self.vars['found_element'] is None:      # 不是通过 “寻找” 这一环节来定位的
                locating_type = self.get_locator_type(ele_loc_str)
                self.waitor.until(lambda d: d.find_element(locating_type,ele_loc_str)).doubleclick()
            else:
                self.vars['found_element'].doubleclick()
                self.vars['found_element']=None


        if action_type=="键盘输入":
            value_on_ele=self.get_value_with_variable(value_on_ele)
            if self.vars['found_element'] is None:      # 不是通过 “寻找” 这一环节来定位的
                locating_type = self.get_locator_type(ele_loc_str)
                self.waitor.until(lambda d: d.find_element(locating_type,ele_loc_str)).send_keys(value_on_ele)
            else:
                self.vars['found_element'].send_keys(value_on_ele)
                self.vars['found_element']=None
        
        if action_type=="键盘输入+回车":
            value_on_ele=self.get_value_with_variable(value_on_ele)
            if self.vars['found_element'] is None:      # 不是通过 “寻找” 这一环节来定位的
                locating_type = self.get_locator_type(ele_loc_str)
                self.waitor.until(lambda d: d.find_element(locating_type,ele_loc_str)).send_keys(value_on_ele+Keys.ENTER)
            else:
                self.vars['found_element'].send_keys(value_on_ele+Keys.Enter)
                self.vars['found_element']=None

        if action_type=="移动相对位移后-点击":
            ActionChains(self.driver).move_by_offset(*eval(value_on_ele)).click().perform()

        if action_type=="移动相对位移后-点右键":
            ActionChains(self.driver).move_by_offset(*eval(value_on_ele)).context_click().perform()

        if action_type=="点击-移动相对位移后-点击":
            if self.vars['found_element'] is None:      # 不是通过 “寻找” 这一环节来定位的
                locating_type = self.get_locator_type(ele_loc_str)
                ele = self.waitor.until(lambda d: d.find_element(locating_type, ele_loc_str))
                ActionChains(self.driver).move_to_element(ele).click().perform()
                self.wait_for_window(3)
                ActionChains(self.driver).move_by_offset(*eval(value_on_ele)).click().perform()
                self.wait_for_window(1)
            else:
                ActionChains(self.driver).move_to_element(self.vars['found_element']).click.perform()
                self.wait_for_window(3)
                ActionChains(self.driver).move_by_offset(*eval(value_on_ele)).click().perform()
                self.wait_for_window(1)
                self.vars['found_element']=None

        if action_type=="点击-移动相对位移后-点右键":
            if self.vars['found_element'] is None:      # 不是通过 “寻找” 这一环节来定位的
                locating_type = self.get_locator_type(ele_loc_str)
                ele = self.waitor.until(lambda d: d.find_element(locating_type, ele_loc_str))
                ActionChains(self.driver).move_to_element(ele).click().perform()
                self.wait_for_window(1)
                ActionChains(self.driver).move_by_offset(*eval(value_on_ele)).context_click().perform()
            else:
                ActionChains(self.driver).move_to_element(self.vars['found_element']).click.perform()
                self.wait_for_window(3)
                ActionChains(self.driver).move_by_offset(*eval(value_on_ele)).context_click().perform()
                self.wait_for_window(1)
                self.vars['found_element']=None 

        if action_type=="右键":
            if self.vars['found_element'] is None:      # 不是通过 “寻找” 这一环节来定位的            
                locating_type = self.get_locator_type(ele_loc_str)
                ele = self.waitor.until(lambda d: d.find_element(locating_type, ele_loc_str))
                ActionChains(self.driver).context_click(ele).perform()
            else:
                ActionChains(self.driver).context_click(self.vars['found_element']).perform()
                self.vars['found_element']=None

        if action_type=="移动到元素后点击":
            if self.vars['found_element'] is None:      # 不是通过 “寻找” 这一环节来定位的
                locating_type = self.get_locator_type(ele_loc_str)
                ele=self.waitor.until(lambda d:d.find_element(locating_type,ele_loc_str))
                ActionChains(self.driver).move_to_element(ele).click().perform()
            else:
                ele=self.vars['found_element']
                ActionChains(self.driver).move_to_element(ele).click().perform()
                self.vars['found_element']=None

        if action_type=="清除输入":
            if self.vars['found_element'] is None:      # 不是通过 “寻找” 这一环节来定位的
                locating_type=self.get_locator_type(ele_loc_str)
                self.waitor.until(lambda d: d.find_element(locating_type,ele_loc_str)).clear()
            else:
                ele=self.vars['found_element']
                self.waitor.until(lambda d: d.find_element(locating_type,ele_loc_str)).clear()
                self.vars['found_element']=None

        if action_type=="寻找":
            '''
            如果action_type=寻找, 从期望值里获得个 elements list, 找到匹配的element 放在变量 self.vars['found_element']中
            action_ty
            '''
            value_on_ele=self.get_value_with_variable(value_on_ele)
            locating_type =self.get_locator_type(ele_loc_str)
            eles=self.waitor.until(lambda d: d.find_elements(locating_type,ele_loc_str))
            for ele in eles:
                if ele.text==str(value_on_ele):
                    self.vars['found_element']=ele
                    break
            if self.vars['found_element'] is None:
                assert False,"Cannot find any element for " + str(value_on_ele)
            
        if action_type=="切换窗口":
            '''
            切换到新窗口
            '''
            self.switch_window(int(ele_loc_str))

        if action_type=="运行js":
            '''
            运行js on element 
            '''
            locating_type =self.get_locator_type(ele_loc_str)
            eles=self.waitor.until(lambda d: d.find_elements(locating_type,ele_loc_str))
            self.driver.execute_script(eles,value_on_ele)

        if action_type=="关闭窗口":
            '''
            close 窗口或者iframe
            '''
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

        if action_type=="关闭浏览器":
            '''
            '''
            self.driver.quit()


    def validator(self,ele_loc_str,compare_method,expectstr):
        if compare_method.strip()=="":
            raise Exception("Failed to get comparasion method")
        else:
            if compare_method =="text_equal_to":
                self.text_equal_to(ele_loc_str,expectstr)
                
            elif compare_method == "text_in_list":
                self.text_in_list(ele_loc_str,expectstr)
            else:
                raise Exception("Failed to recognize comparasion method")
            

    def text_equal_to(self,ele_loc_str,textinput):
        '''
            判断element 文本是否与输入的文本相同
        '''
        locating_type=self.get_locator_type(ele_loc_str)
        ele_text=self.waitor.until(lambda d: d.find_element(locating_type,ele_loc_str)).text
        print("Current Display: " + ele_text)
        print("Expect: "+textinput)
        assert ele_text == textinput

    def text_in_list(self,ele_loc_str,textinput):
        '''
            判断 输入的文本 是否再elements 列表里
        '''
        locating_type=self.get_locator_type(ele_loc_str)
        eles=self.driver.find_elements(locating_type,ele_loc_str)
        ele_text=[]
        for x in eles:
            ele_text.append(x.text)
        print("Current List:")
        print(ele_text)
        print("Search for: "+textinput)
        assert textinput in ele_text

    def switch_window(self,win_handle_var):
        if win_handle_var!=0:     # 0 不切换, 其他数字是 窗口数组 的索引值
            self.driver.switch_to.window(self.driver.window_handles[win_handle_var])