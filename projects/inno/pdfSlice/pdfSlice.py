from os import chdir
from os.path import dirname, abspath
from pikepdf import Pdf
import pandas as pd
from myfuc import cpath


chdir(dirname(abspath(__file__)))
useCols = ['國品字號', '公司名稱(中文)\n如有異動，請以括號備註原申請公司名稱', '項目名稱(中文)\n如有異動，請以括號備註原申請項目名稱']
pd.set_option('display.max_columns', None)
sheet = {'產品類': '產品類(566)', '服務類': '服務類(394)', '產品類1213': '產品類1213'}
per = {'產品類': 6, '服務類': 6, '產品類1213': 6}
num = {'產品類': 4, '服務類': 3, '產品類1213': 1}


def pdfSplit(pdfInfo):
    i = 0
    pages = pdfInfo.pdf.pages
    per = pdfInfo.per
    for index, row in pdfInfo.df.iterrows():
        p = index // 150 + 1
        output = Pdf.new()
        code = row.國品字號.replace(' ', '')
        try:
            for j in range(per):
                output.pages.append(pages[i + j])
            output.save(f'{cpath(f"secret/output/{pdfInfo.name}/p{p}/{code}")}/{code}.pdf')
        except IndexError:
            break
        i = i + per


class MyPdf:
    def __init__(self, name) -> None:
        self.name = name
        self.per = per[name]
        self.df = pd.read_excel(f'secret/2022續審有無異動名單(分類).xlsx', sheet_name=sheet[self.name], usecols=useCols)
        #self.pdf = Pdf.open(f'secret/合併列印/SNQ國家品質標章授權合約書({self.name}全).pdf')
        self.pdf = Pdf.open(f'secret/合併列印/{self.name}.pdf')


def main1():
    for pdf in [MyPdf(name) for name in ['產品類1213']]:
        pdfSplit(pdf)


class Combine:
    def __init__(self, cat) -> None:
        self.cat = cat
        self.n = num[cat] + 1
        self.df = pd.concat([pd.read_excel('secret/2022續審通過授權約定書.xlsx', sheet_name=f'{cat}{i}') for i in range(1, self.n)])
        self.df = self.df.drop(self.df[self.df.Type != 'Folder'].index)[['Name', 'URL']]


def main2():
    writer = pd.ExcelWriter('secret/2022續審通過授權約定書_url.xlsx', engine='xlsxwriter')
    for data in [Combine(cat) for cat in ['服務類', '產品類', '產品類1213']]:
        data.df.to_excel(writer, sheet_name=data.cat, index=False)
    writer.close()


if __name__ == '__main__':
    main2()
