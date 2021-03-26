from selenium import webdriver
from PyQt5.QtWidgets import QMainWindow, QTextEdit

import time, json


class PanicBuying():
    def __init__(self):
        self.start_kg = False
        self.close_all = False

    def start(self, name, driver, ms, url, tab_items, time_wait, wait, refresh):
        '''
        开始自动多线程抢购
        '''
        try:
            # 超时
            driver.set_page_load_timeout(5000)  # 防止页面加载个没完
            driver.get(url)
            textTrues = []  # 存已经找到的目标
            times=time.localtime()
            millisecond =int(time_wait.split('.')[-1])
            start_time=int(time.mktime(time.strptime(f'{times.tm_year}-{times.tm_mon}-{times.tm_mday} {time_wait}',
                                          "%Y-%m-%d %H:%M:%S.%f")) * 1000) + millisecond
            print(start_time)

            # 判断是否需要等待
            if wait == True:
                # 如果需要则循环等待这个时间到来,注意了这是电脑时间
                ms.log_add.emit(f'浏览器:{name} 自动启动时间为:{time_wait}')
                while True:
                    if int(round(time.time() * 1000)) >= start_time:
                        self.start_kg = True
                        ms.log_add.emit('True')#信号
                        ms.log_add.emit(f'浏览器:{name} 时间到达!开始运行!')
                        break

            # 判断是否需要刷新
            if refresh == True:
                ms.log_add.emit(f'浏览器:{name} 刷新!')
                driver.refresh()

            def element_css(selector_text: str, wz_text: str):
                '''
                利用css寻找目标,然后操作
                :return:
                '''
                print(wz_text)
                if wz_text.find('##') != -1:

                    #将浏览器滚动条拖动到最下方,这样就会加载
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    time.sleep(0.01)
                wz=wz_text.replace('##', '')
                an = driver.find_element_by_css_selector(selector_text)
                # 判断操作类型,这种为输入模式
                if wz.find('$$') != -1:
                    # 输入文字
                    wz = wz.replace('$$', '')
                    an.send_keys(wz)
                    ms.log_add.emit(f'浏览器:{name} 成功帮忙输入了{wz} {driver.title}')
                    return True
                # 判断操作类型这种位可以直接点击的,并不用等待
                elif wz.find('%%') != -1:
                    # 直接点击
                    wz = wz.replace('%%', '')
                    an.click()
                    ms.log_add.emit(f'浏览器:{name} 点击{wz}按钮成功! {driver.title}')
                    return True
                else:
                    # 点击按钮
                    an.click()
                    if wz not in textTrues :
                        ms.log_add.emit(f'浏览器:{name} 通过CSS定位到{wz}按钮 {driver.title}')
                        textTrues.append(wz)
                return False


            def element_text(selector_text: str):
                '''
                利用text寻找目标,然后进行操作
                :return:
                '''
                if selector_text.find('##') != -1:
                    #将浏览器滚动条拖动到最下方,这样就会加载
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    time.sleep(0.01)
                r_text = selector_text.replace('##', '')
                # 判断操作类型
                if r_text.find('%%') != -1:
                    # 直接点击
                    r_text = r_text.replace('%%', '')
                    an = driver.find_element_by_xpath(f"//*[text()='{r_text}']")

                    an.click()
                    ms.log_add.emit(f'浏览器:{name} 点击{r_text}按钮成功! {driver.title}')
                    return True
                else:
                    an = driver.find_element_by_xpath(f"//*[text()='{r_text}']")
                    an.click()
                    if r_text not in textTrues:
                        ms.log_add.emit(f'浏览器:{name} 通过名字定位到{r_text}按钮 {driver.title}')
                        textTrues.append(r_text)


            def find_isTrue(wz_text: str):
                '''
                判断是否是成功
                :return:
                '''
                #如果在点击成功列表里面,则发出点击成功信号
                r_text = wz_text.replace('##', '')
                if r_text in textTrues:
                    ms.log_add.emit(f'浏览器:{name} 点击{r_text}按钮成功! {driver.title}')
                    return True
                else:
                    return False
            def run_isOrNO():
                '''
                判断是否继续需要暂停
                :return:
                '''
                while self.start_kg == False:
                    # 判断是否要退出
                    if self.close_all == True:
                        ms.log_add.emit(f'浏览器:{name} 已被强制关闭! {driver.title}')
                        return
                    time.sleep(0.01)

            # 正式开始
            length = tab_items.rowCount()
            for i in range(length):
                try:
                    try:
                        store = tab_items.item(i, 0).text()
                    except:
                        store = ''
                    try:
                        text = tab_items.item(i, 1).text()
                    except:
                        text = ''
                    try:
                        css = tab_items.item(i, 2).text()
                    except:
                        css = ''
                    print(store,css,text)

                    #如果暂停了,就卡死不动
                    run_isOrNO()
                    # 优先用css来定位
                    if css != '' :
                        # 尝试用css定位,如果定位成功则点击,如果定位失败则尝试使用text
                        # 直到点击成功后再下一个目标
                        while True:
                            time.sleep(0.01)
                            # 如果暂停了,就卡死不动
                            run_isOrNO()

                            try:
                                # 尝试寻找并且尝试操作 如果是输入框或者不需要等待的按钮,,完成后就直接跳出
                                if element_css(css, text) == True:
                                    break
                            except:
                                try:
                                    # 尝试寻找并且尝试操作
                                    element_text(text)
                                except:  # 操作失败,可能是没找到或者是已经点成功了
                                    # 判断是否是成功
                                    if find_isTrue(text) == True:
                                        break
                    # 如果没有css则考虑直接使用text来搜索定位.
                    elif text != '' :
                        while True:
                            time.sleep(0.01)
                            # 如果有多个页面,则循环进行
                            # 如果暂停了,就卡死不动
                            run_isOrNO()
                            try:
                                # 尝试寻找并且尝试操作
                                element_text(text)
                            except:#操作失败,可能是没找到或者是已经点成功了
                                # 判断是否是点击成功
                                if find_isTrue(text) == True:
                                    break
                    else:
                        ms.log_add.emit(f'浏览器:{name} 脚本配置错误!')
                    #更新一下长度,为了适应,突然增加的长度
                    length = tab_items.rowCount()

                except:
                    ms.log_add.emit(f'发生错误,应该是配置被临时删除,导致了设置数据丢失!')

        except Exception as err:
            print(err)
            ms.log_add.emit(f'浏览器:{name} 意外关闭!')
