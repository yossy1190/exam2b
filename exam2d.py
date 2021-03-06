import os
from re import I
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import datetime

# Selenium4対応済

def set_driver(hidden_chrome: bool=False):
    '''
    Chromeを自動操作するためのChromeDriverを起動してobjectを取得する
    '''
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if hidden_chrome:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(f'--user-agent={USER_AGENT}') # ブラウザの種類を特定するための文字列
    options.add_argument('log-level=3') # 不要なログを非表示にする
    options.add_argument('--ignore-certificate-errors') # 不要なログを非表示にする
    options.add_argument('--ignore-ssl-errors') # 不要なログを非表示にする
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # 不要なログを非表示にする
    options.add_argument('--incognito') # シークレットモードの設定を付与
    
    # ChromeのWebDriverオブジェクトを作成する。
    service=Service(ChromeDriverManager().install())
    return Chrome(service=service, options=options)



'''
ログファイルを格納するディレクトリを作成
'''
def make_dir(dir_path:str) :
    os.makedirs(dir_path,exist_ok=True)
make_dir("C:/Users/Yoshi/Project2/log_files")





def main():
    '''
    main処理
    '''
    search_keyword =input("検索キーワードを入力してください >>> ")
    # driverを起動
    driver = set_driver()
    
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(3)
    
    '''
    ポップアップを閉じる
    ※余計なポップアップが操作の邪魔になる場合がある
      モーダルのようなポップアップ画面は、通常のclick操作では処理できない場合があるため
      excute_scriptで直接Javascriptを実行することで対処する
    '''
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(3)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')


 
    # find_elementでHTML要素(WebElement)を取得する
    # byで、要素を特定する属性を指定するBy.CLASS_NAMEの他、By.NAME、By.ID、By.CSS_SELECTORなどがある
    # 特定した要素に対して、send_keysで入力、clickでクリック、textでデータ取得が可能
 
    # 検索窓に入力
    driver.find_element(by=By.CLASS_NAME, value="topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element(by=By.CLASS_NAME, value="topSearch__button").click()


    
    # find_elements(※複数形)を使用すると複数のデータがListで取得できる
    # 一覧から同一条件で複数のデータを取得する場合は、こちらを使用する
    
 
 
    # 空のDataFrame作成
    df = pd.DataFrame()
    
    '''
    ログ記録における件数カウントとしてcounterという変数を作成。
    '''
    counter=1
    # while trueにより、exceptでbreakするまで無限ループ
    while True:
        recruit_articles=driver.find_elements(by=By.CSS_SELECTOR,value=".cassetteRecruit__heading.cassetteUseFloat")
        # if len(recruit_articles)>=1:
        for recruit_article in recruit_articles: 
            '''
            １ページ分のクロール処理部分をtryで囲う。findできなかったら、exceptでエラーを補足
            '''
            try:
                name_elm = recruit_article.find_element(by=By.CLASS_NAME, value="cassetteRecruit__name")
                copy_elm = recruit_article.find_element(by=By.CLASS_NAME, value="cassetteRecruit__copy.boxAdjust")
                print(name_elm.text,copy_elm.text)
                df = df.append(
                    {"会社名": name_elm.text,
                    "キャッチコピー":copy_elm.text}, 
                    ignore_index=True)
                '''
                成功処理ログを記録。"a"で記録することで、末尾に記録していく。
                '''
                with open("C:/Users/Yoshi/Project2/log_files/log_file.txt", 'a', encoding='utf-8_sig') as f:
                    f.write(f"処理{counter}番目:OK\n")
                    counter+=1
            except  :
                '''
                失敗ログを記録。errorの場合でも、for文の
                '''
                with open("C:/Users/Yoshi/Project2/log_files/log_file.txt", 'a', encoding='utf-8_sig') as f:
                    f.write(f"処理{counter}番目:NG\n")
                counter+=1
        '''
        次のページボタンを取得。１つ以上あれば、if関数内の処理を実行。存在しなければ、最終ページと判断。
        '''
        next_pages=driver.find_elements(by=By.CLASS_NAME, value=".iconFont--arrowLeft")
        if next_pages:
            next_pages[0].click()
            
            # 読み込みを完了させるため、sleepを起動
            time.sleep(2)
        
        else:
            print("最終ページです")
            break
                        
    # #ＣＳＶに書き出す。
    df.to_csv("採用案件一覧.csv",encoding="utf-8_sig")
    


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
