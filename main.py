from DrissionPage import SessionPage, ChromiumPage
import pandas as pd
import logging
import shutil
import time
import os


logging.basicConfig(filename='log.txt',
                    format = '%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def logprint(msg:str):
    """
    日志打印
    :param msg: 信息
    """
    logging.info(msg)
    print(msg)

def get_data(marketCode:str | None):
    """
    获取数据
    :param marketCode: 市场代码
    """
    # 打开网页
    logprint(f'正在爬取{marketCode}...')
    page = SessionPage()
    page.get('http://ncpscxx.moa.gov.cn/product/piMarketPrice/getMarketDatas',
             params={'marketCode': marketCode})

    # 网页转换为json格式
    json = page.json['data']

    # 时间戳
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    if marketCode is None:
        marketCode = 'None'

    # 如果data文件夹不存在，就创建文件夹
    if not os.path.exists('data'):
        os.mkdir('data')

    if not os.path.exists(f'data/{marketCode}'):
        os.mkdir(f'data/{marketCode}')

    # 如果csv文件存在，就删除文件后再爬取
    if os.path.exists(f'data/{marketCode}/{today}.csv'):
        os.remove(f'data/{marketCode}/{today}.csv')

    # 用pandas读取json数据，并以csv格式保存
    df = pd.DataFrame(json)
    df.to_csv(f'data/{marketCode}/{today}.csv', index=False, encoding='utf_8_sig')

    logprint(f"'data/{marketCode}/{today}.csv' 已保存!")

def backup(marketCode:str | None):
    """
    备份数据
    :param marketCode: 市场代码
    """
    # 时间戳
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    now = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))

    if marketCode is None:
        marketCode = 'None'

    # 如果backup文件夹不存在，就创建文件夹
    if not os.path.exists('backup'):
        os.mkdir('backup')

    if not os.path.exists(f'backup/{marketCode}'):
        os.mkdir(f'backup/{marketCode}')

    # 将today.csv复制到backup文件夹，以now.csv命名
    shutil.copy(f'data/{marketCode}/{today}.csv', f'backup/{marketCode}/{now}.csv')

    logprint(f"'data/{marketCode}/{today}.csv' 已备份!")
    logprint(f"'data/{marketCode}/{today}.csv' -> backup/{marketCode}/{now}.csv'")
    logprint('----------------------------------------------------------')

def main(minute:int, network_username:str, network_password:str):
    """
    主函数
    :param minute: 爬取时间间隔，单位为分钟
    :param network_username: 账号
    :param network_password: 密码
    """
    while True:
        try:
            # 无锡朝阳农产品批发市场
            marketCode = '3202014'
            get_data(marketCode)
            backup(marketCode)

            # 无锡市某农产品批发市场
            marketCode = None
            get_data(marketCode)
            backup(marketCode)

            time.sleep(60*minute)
        except:
            logprint('出问题了！\n正在重试...')
            time.sleep(5)


if __name__ == '__main__':
    minute=20
    network_username='17391159242'
    network_password='031531'

    main(minute, network_username, network_password)