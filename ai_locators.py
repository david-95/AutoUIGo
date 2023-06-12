  
from aip import AipOcr

class AIOcrWorker():
    '''
    未完， 想通过图片识别 AI 来进行界面的测试
    '''
 
    def __init__(self) -> None:
        pass
  
   
    def get_file_content(self,filePath):
      with open(filePath, "rb") as fp:
         return fp.read()

    image = get_file_content('文件路径')
    url = "https//www.x.com/sample.jpg"
   
	##调用通用文字识别（标准含位置信息版）
    res_image = client.general(image)
    res_url = client.generalUrl(url)
   print(res_image)
   print(res_url)

	//如果有可选参数
   options = {}
   options["recognize_granularity"] = "big"
   options["language_type"] = "CHN_ENG"
   options["detect_direction"] = "true"
   options["detect_language"] = "true"
   options["vertexes_location"] = "true"
   options["probability"] = "true"
   res_image = client.general(image, options)
   res_url = client.generalUrl(url, options)
   print(res_image)
   print(res_url)