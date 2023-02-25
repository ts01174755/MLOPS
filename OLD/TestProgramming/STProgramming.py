import os

from tqdm import tqdm
from dotenv import load_dotenv, find_dotenv
import openai

load_dotenv(find_dotenv('../../env/.env'))
openai.api_key = os.getenv("OPENAI_API_KEY")

if __name__ == '__main__':
    # Set up the model and prompt
    '''拆解關鍵字'''
    prompt = """以下是一個高中考題：
        "下列所述光電效應中入射光與光電子之間的關係，何者證實了光 具有粒子性?
        (A)光電子的數目與照射在金屬表面的入射光頻率成正比 
        (B)光電子産生與否決定於照射在金屬表面的入射光強度 
        (C)照射於金屬表面的入射光頻率須大於某一特定值方能産生光電子 
        (D)照射於金屬表面的入射光波長須大於某一特定值方能産生光電子 
        (E)照射於金屬表面的入射光波長及強度均須大於某一特定值方能産生光電子"
        請幫我萃取關鍵字，回答我的格式如下："關鍵字：xxx、xxx"
    """
    # completion = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=prompt,
    #     max_tokens=1024,
    #     top_p=1,
    #     stop=None,
    #     temperature=1,
    # )
    # response = completion.choices[0].text
    # skipStrs = ['關鍵字', '答案', '答', '：', '。', '，', "\n", "：", "Answer"]
    # for str_ in skipStrs:
    #     response = response.replace(str_, '')
    # responseList = response.split('、')
    # print(responseList)

    '''關鍵字知識'''
    key_value = {
        '光電效應': '光電效應是指光被一個外加電場影響，而誘發物質產生電荷分佈的一種物理現象。它是一種微觀量子現象，在對物質施加微弱的薄膜外加電場時，產生微小的电流，主要有四種光電效應，分別是熱散射效應、顫動效應、多普勒效應和霍爾效應。這些光電效應在能源技術發展中扮演著重要的角色，它應用於太陽能電池、光纖通訊、雷射技術和其他光技術中。',
        # '入射光': '入射光是指從外部來到光源，可以是一個機構或一條光線，會經過一個物體的穿透性表面，到達物件的另一面的光線。入射光可以用不同光源提供，包括太陽，陽光和其他光源。這些光源會投射大量的光，用於顯示該物件的形狀，表面形質，顏色以及它的物理性質。入射光也可以提供信息，用於檢測，影像，醫學診斷等檢測應用。',
        '光電子': '光電子是指用光輸入和輸出資料的電子產品，可以被用於攝影、影像、音頻和輸送等。基本上它可以用於將數據從一台電腦傳輸到另一台電腦，甚至從某一網路到另一網路。它可以使用光纖線通過光學的技術在兩點之間傳送信號，需要低功耗、高效率、高速度和低衰減。另外，它還可以幫助改善傳統的電子產品，包括摄像機、多媒體和傳感器。',
        # '照射': '照射是指物質吸收從外部來源中釋放的能量，一般照射有熱照射和無線照射。熱照射是指物質吸收外部來源中釋放的熱能，其中的熱量來自它的移動粒子，例如太陽照射的熱量來自太陽發出的微粒；無線照射是指物質吸收從外部來源中釋放出的非熱能量，包括電磁照射、凝視照射、紫外照射等等。電磁照射是指物質吸收通過空間傳播的電磁波，例如日光和電視信號等生物體的放射性照射是指物質吸收從核反應發出的放射性能量，其中的能量來自放射性物質發出的射線，但不包括X射線放射所产生的熱能。',
        # '金屬表面': '金屬表面本質上是由金屬原子所構成的，它因此具有均勻的表面結構，並且可以產生一層氧化膜，使其具有較高程度的耐腐蝕性。它具有良好的導熱性和導電性，有著低的摩擦系數，但也容易沉積化合物和污染物。金屬表面也可以藉由化學轉換程序，例如氧化披覆、轉印或塗上磷化處理，來改變表面的結構和特性。',
        '頻率': '頻率是指在特定接收機（或發射機）下，一定時間內波段中信號的總和。它量度的是每秒某個頻帶中可用的信號數量，它與輻射的波長和波數等有關。頻率的單位時Hz（赫茲），它也被稱為“頻率因數”或“頻率量”。該單位用於表示信號波的總和的數量，以及它每秒經過接收機或發射機的頻率。',
        # '強度': '強度往往指的是材料或物件的承受各種類型的價值，例如抗壓強度、弯曲強度以及抗拉強度。另一個更加普遍包含的定義是材料對外界事件的抵抗能力，如侵蝕、損壞以及熔化。 抗壓強度（Compressive Strength）指物體對壓力的耐受力，是激發物件的把力且導致材料的壓縮的能力。弯曲強度（Flexural Strength）指物體的介面能抵抗力，可知材料對於弯曲力是有多大的抗衡能力。抗拉強度（Tensile Strength）指物件對於拉力的耐受力，用於衡量材料對於拉力的抵抗能力。',
        '波長': '波長（Wavelength）是指波擴散而成時，有浪起伏印記的一段距離，或者指振動波的波長距離。比如說，聲音波的波長是空間內的聲音波的最小距離。波長的長短依據不同的媒質而有所不同，比如說水通常會慢很多，這就意味在水中的波長比在空氣中的長很多。'
    }
    # key_value = {_: '' for _ in responseList}
    # for key_ in tqdm(key_value.keys()):
    #     completion = openai.Completion.create(
    #         engine="text-davinci-003",
    #         prompt=f"請簡述有關{key_}的知識",
    #         max_tokens=512,
    #         top_p=1,
    #         stop=None,
    #         temperature=1,
    #     )
    #     response = completion.choices[0].text
    #     key_value[key_] = response.replace('\n','')
    # print(key_value)

    '''產出題目'''
    responseText = ['1.什麼是光電效應？', '2.以何種物理現象誘導物質產生電荷分佈？', '3.什麼是光電子？', '4.光電子可用於什麼？', '5.什麼是頻率？', '6.頻率以何種單位表示？', '7.什麼是波長？', '8.波長會因該媒質影響而有所差異，為什麼？', '9.多普勒效應是什麼？', '10.在光電效應中，什麼是熱散射效應？', '11.霍爾效應常用於什麼？', '12.光纖通過什麼技術來在兩點之間傳送信號？', '13.摄像機、多媒體和傳感器能從光電子中受益嗎？', '14.何種光電效應在能源技術中扮演著重要的角色？', '15.該單位Hz也被稱為什麼？', '16.什麼是多普勒效應？', '17.以何種微觀量子現象產生微小的电流？', '18.為什麼需要使用光電子？', '19.傳送信號的極靜的屬性為何？', '20.為什麼霍爾效應被用於光纖通訊？']
    promtPre = ""
    for key_ in key_value: promtPre += f"'{key_}': '{key_value[key_]}';\n"
    promptALL = f"""給你一份專有名詞的知識如下：\n{promtPre}請利用這些知識出20題題目，不必包含選項。"""
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=promptALL,
        max_tokens=2048,
        top_p=1,
        stop=None,
        temperature=1,
    )
    response = completion.choices[0].text
    responseText = response.split('\n')
    print(promptALL)
    print(response)
    print(responseText)

    '''題目展開'''
    '''選項展開'''

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
