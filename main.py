import json
import os
from datetime import datetime, timedelta

import requests
import yagmail
from bs4 import BeautifulSoup


def nowT():
    return (datetime.utcnow() + timedelta(hours=8)).strftime('%Y/%m/%d %H:%M:%S')

def str2bool(s):
    if s=='true':
        return True
    elif s=='false':
        return False


class SurfaceWatchDog:
    def __init__(self):
        self.stock_url = 'https://www.microsoftstore.com.cn/certified-refurbished-surface-pro-8-configurate'
        self.attrDict = {'5483': '亮铂金',
                         '5919': '石墨灰',
                         '5926': '英特尔酷睿 i5/8GB/128GB',
                         '5927': '英特尔酷睿 i5/8GB/256GB',
                         '5928': '英特尔酷睿 i5/16GB/256GB',
                         '5929': '英特尔酷睿 i5/8GB/512GB',
                         '5930': '英特尔酷睿 i7/16GB/256GB',
                         '5931': '英特尔酷睿 i7/16GB/512GB',
                         '5932': '英特尔酷睿 i7/16GB/1TB',
                         '5933': '英特尔酷睿 i7/32GB/1TB'}
        self.session = requests.session()
        self.onlyOnSale = True
        self.m_filter = []
        self.senderMail = {}
        self.rcvMails = []
        self.loadConf()
        self.yag = yagmail.SMTP(user=self.senderMail['addr'], password=self.senderMail['passwd'],
                                host=self.senderMail['host'],
                                port=self.senderMail['port'], smtp_ssl=False)

    def loadConf(self):
        try:
            conf = os.environ.get('conf')
            if not conf:
                print(nowT() + "|配置有误...")
                exit(-1)
            jConf = json.loads(conf)
            self.m_filter = jConf['m_filter']
            self.senderMail = jConf['senderMail']
            self.rcvMails = jConf['rcvMails']
            self.onlyOnSale = str2bool(jConf['onlyOnSale'])
        except Exception as e:
            print(nowT() + e)
            exit(-1)

    @staticmethod
    def genItem(device, color, sku, price, onSale):
        return {'device': device, 'color': color, 'sku': sku, 'price': price, 'onSale': onSale}

    def query(self):
        res = self.session.request(url=self.stock_url, method='get')
        if res.status_code != 200:
            print("Error to browser Microsoft Store.")
        if res:
            soup = BeautifulSoup(res.text, "html.parser")
            script = soup.findAll('script', type='text/x-magento-init')[16]
            tarScript = json.loads(script.text)
            onSales = \
                tarScript['[data-role=swatch-options]']['IsobarCommerce_BundleSwatches/js/swatch-renderer'][
                    'jsonConfig'][
                    'mainProducts']
            return onSales

    def getOnSale(self, devices: dict, isOnSale: bool, _filter: list = None):
        onSales = []
        types = ['30', '20', '15']
        try:
            for t in types:
                for device in devices[t]:
                    item = devices[t][device]
                    if not isOnSale or item['is_saleable']:
                        device = self.genItem(item['attributes']['specification'],
                                              item['attributes']['color'],
                                              item['sku'],
                                              item['selection_price_value'],
                                              item['is_saleable'])
                        if not _filter or device['color'] in _filter[0] and device['device'] in _filter[1]:
                            onSales.append(device)
                return onSales

        except Exception as e:
            print(e)

    def printDevice(self, devices: list):
        print('%-22s%-6s\t%-10s\t%-20s\t%-12s' % ('查询时间', '有货', '颜色', '规格', '价格'))
        if len(devices) == 0:
            print(nowT() + "|无货")
            return
        for device in devices:
            content = '%-22s\t%-6s\t\t%-10s%-20s\t%-12s' % (
                nowT(), device['onSale'], self.attrDict[device['color']],
                self.attrDict[device['device']], device['price'])
            print(content)
            self.notify(content)

    def notify(self, txt):
        self.yag.send(self.rcvMails, '微软Surface已补货', txt)


if __name__ == '__main__':
    dog = SurfaceWatchDog()
    allDevices = dog.getOnSale(dog.query(), dog.onlyOnSale, dog.m_filter)
    dog.printDevice(allDevices)
