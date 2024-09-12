import pyautogui
import cv2
import numpy as np
import math
import win32gui  
  
def has_num(num, num_set=None):  
    if num_set is None:  
        num_set = set()  
  
    for existing_num in num_set:  
        if abs(existing_num - num) < 8:  
            return True  
  
    num_set.add(num)  
    return False
    
def find_and_print_matches(template_path, snap_region, match_threshold=0.8):
    """
    在屏幕上查找目标图片并打印所有匹配结果的位置。
    Args:
        template_path: 目标图片的路径。
        match_threshold: 匹配阈值，默认值为 0.8。
    """
    # 加载目标图片
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    # 获取屏幕截图
    screenshot = pyautogui.screenshot(region=snap_region)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
 
    # 使用模板匹配查找目标图片
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
 
    # 获取匹配结果
    match_locations = np.where(result >= match_threshold)
 
    # 如果找到匹配结果
    if len(match_locations[0]) > 0:
        num_set = set()
        for i in range(len(match_locations[0])):
            match_x = match_locations[1][i] + snap_region[0]
            match_y = match_locations[0][i] + snap_region[1]
            distance = match_x+ match_y   
            if has_num(distance,num_set):
                continue
            print(f"位置：({match_x}, {match_y})，距离：{distance:.2f}")
            #pyautogui.moveTo(match_x + 20, match_y + 28)
            pyautogui.click(match_x + 20, match_y + 30)
        return True
    else:
        return False
 
def find_window_by_title(title):
    #通过窗口标题查找窗口句柄  
    hwnd = win32gui.FindWindow(None, title)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)  
    return left, top      
   
# 示例代码
if __name__ == "__main__":

    #鼠标点击间隔
    pyautogui.PAUSE = 0.01
    
    #TelegramDesktop窗口大小 400 * 700
    #截图位置
    left, top = find_window_by_title("TelegramDesktop")
    snap_region = (left, top, 400, 700)
  
    # 目标图片路径
    target_list = {"target.png", "target1.png"}
    play = "play.png"
    
    #循环截图点击
    no_find_count = 0;
    clickcount = 0;
    threshold = 0.8
    while True:
        clickcount += 1
        #用下面的阈值会漏部分
        #threshold = 0.8 if clickcount % 9 == 0 else 1
        
        for item in target_list:
            if find_and_print_matches(item, snap_region, threshold):
                pass
            else:
                print("未识别目标")
                no_find_count += 1
        
        #50次没找到尝试重新点play,不用自动执行下一次可以屏蔽
        if no_find_count > 50:
            print("try play")
            find_and_print_matches(play, snap_region)
            no_find_count = 0
           
           
