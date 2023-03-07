import os; import sys;
if len(sys.argv) > 1:
    os.chdir(sys.argv[1])
    sys.path.append(os.getcwd())
from package.common.MLFlow import MLFlow
from package.common.DockerCmd import DockerCmd
from package.common.DatabaseCtrl import MongoDBCtrl
from DE_MongoDB.package.STCrawler import STCrawler
from dotenv import load_dotenv, find_dotenv



# # 設定目標網站的URL
# url = 'https://www.amazon.com/dp/B08J7V1PBK/'
#
# # 發送GET請求到目標網站
# response = requests.get(url)
#
# # 使用BeautifulSoup解析網頁內容
# soup = BeautifulSoup(response.text, 'html.parser')
#
# # 從解析後的網頁中找出我們需要的元素，例如商品價格和評價
# price = soup.find('span', {'class': 'a-price-whole'}).text
# rating = soup.find('span', {'class': 'a-icon-alt'}).text
#
# # 將爬取到的結果輸出
# print('商品價格：', price)
# print('商品評價：', rating)



if __name__ == '__main__':
    print('Here is MongoCrwaler')

    # 連接MongoDB
    # load_dotenv(find_dotenv('env/.env'))
    stCrawler = MLFlow(STCrawler())

    stCrawler.get_st_all_data()
    #
    # # 新增collection - 等價於建立table
    # print(mongodb.create_collection('test'))
    #
    # # 新增document - 等價於建立row
    # print(mongodb.insert_document('test', {'name': 'Peter', 'age': 18}))
    #
    # # 查詢document - 等價於查詢row
    # print(mongodb.find_one_document('test', {'name': 'Peter'}))
    #
    # # 更新document - 等價於更新row
    # print(mongodb.update_document('test', {'name': 'Peter'}, {'$set': {'age': 19}}))
    #
    # # 查詢document - 等價於查詢row
    # print(mongodb.find_one_document('test', {'name': 'Peter'}))
    #
    # # 刪除document - 等價於刪除row
    # print(mongodb.delete_document('test', {'name': 'Peter'}))
    #
    # # 刪除collection - 等價於刪除table
    # print(mongodb.drop_collection('test'))
