import json,os,requests,re,subprocess,time
from shutil import copyfile,rmtree

class DownloadMusic():
    """
    音乐下载、处理相关类
    """

    def __init__(self,path:str,PlaylistName:str) -> None:
        """
        path:输出文件夹的名称(创建在py文件同目录)
        PlaylistName:歌单(子文件夹)的名称
        """
        self.RunPath = os.path.dirname(os.path.realpath(__file__))
        self.OutputPath = self.RunPath + '\\' + path
        self.TempPath = self.OutputPath + '\\temp'
        self.DownloadPath = self.OutputPath + '\\' + PlaylistName
        self.header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

        if os.path.exists(self.OutputPath) == False:
            os.mkdir(self.OutputPath)
        if os.path.exists(self.TempPath)  == False:
            os.mkdir(self.TempPath)
        if os.path.exists(self.DownloadPath)  == False:
            os.mkdir(self.DownloadPath)
    
    def Download(self,SongData:dict) -> bool:
        """
        传入包含歌曲数据的字典
        根据传入的数据确定下载方式并合成最终的文件
        """

        #读取必要的数据

        #歌曲源
        SongSource = SongData.get('source', '未知来源')
        #歌曲名称
        SongName = SongData.get('title', '未知名称')
        #歌曲作者
        SongArtist = SongData.get('artist', '未知作者')
        #歌曲专辑
        SongAlbum = SongData.get('album', '未知专辑')
        #歌曲链接
        SongUrl = SongData.get('source_url', '未知链接')
        #歌曲封面链接
        SongCoverUrl = SongData.get('img_url', '未知封面链接')
        #把非法字符去掉
        SongFileName = re.sub(r'[\\/:"*?<>|]', '', SongName)

        print(f"正在从 {SongSource} 下载 {SongName}")

        SongFileName = re.sub(r'[\\/:"*?<>|]', '', SongName)
        if os.path.exists(rf'{self.DownloadPath}\{SongFileName}.mp3'):
            print("歌曲已存在，跳过下载")
            return True

        #根据歌曲源下载歌曲
        if SongSource == 'netease':
            #提取网易云音乐的id
            SongID = int(re.search(r'id=(\d+)', SongUrl).group(1))
            #转换为下载链接
            SongUrl = f'http://music.163.com/song/media/outer/url?id={SongID}.mp3'
            #下载
            if self.DownloadFile(SongUrl,self.TempPath+'\\input.mp3') == False:
                print('下载失败：下载歌曲失败')
                return False
            
        elif SongSource == 'qq':
            #提取QQ音乐的mid
            SongID:str = re.search(r'mid=([A-Za-z0-9]+)&', SongUrl).group(1)
            #转换为下载链接
            SongUrl = self.GetQQUrl(SongID)
            if SongUrl == None:
                print("下载失败：下载链接获取失败")
                return False
            #下载
            if self.DownloadFile(SongUrl,self.TempPath+'\\input.m4a') == False:
                print('下载失败：下载歌曲失败')
                return False
            
            #转换为mp3
            command = [rf'{self.RunPath}\ffmpeg.exe',
            '-i',rf'{self.TempPath}\input.m4a',
            rf'{self.TempPath}\input.mp3']
            nowtime = time.strftime('%H:%M:%S', time.localtime(time.time()))
            with open('log.txt','a',encoding='utf-8') as log:
                subprocess.run(command,input=b'y\n',stdout=log,stderr=log)
                log.write(f'[{nowtime}]\n\n')
            

        else:
            print('下载失败：不支持的平台')
            return False

        #下载封面
        if self.DownloadFile(SongCoverUrl,self.TempPath+'\\cover.jpg') == False:
            print('下载失败：下载封面失败')
            return False
        
        #用ffmpeg合成音频文件
        command = [rf'{self.RunPath}\ffmpeg.exe',
            '-i',rf'{self.TempPath}\input.mp3',
            '-i',rf'{self.TempPath}\cover.jpg',
            '-map','0:0','-map','1:0','-c','copy','-id3v2_version','3',
            '-metadata',f'title={SongName}',
            '-metadata',f'artist={SongArtist}',
            '-metadata',f'album={SongAlbum}',
            rf'{self.TempPath}\output.mp3']

        nowtime = time.strftime('%H:%M:%S', time.localtime(time.time()))
        with open('log.txt','a',encoding='utf-8') as log:
            subprocess.run(command,input=b'y\n',stdout=log,stderr=log)
            log.write(f'[{nowtime}]\n\n')

        #复制文件到歌单目录下
        copyfile(rf'{self.TempPath}\output.mp3',rf'{self.DownloadPath}\{SongFileName}.mp3')

        print('下载成功')
        return True
    
    def GetQQUrl(self,SongID:str) -> str:
        """
        通过QQ音乐的mid获取下载链接
        格式为m4a
        """
        #拼接url
        QQAPI = "https://u.y.qq.com/cgi-bin/musicu.fcg?format=json&data=%7B%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%22358840384%22%2C%22songmid%22%3A%5B%22{}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%221443481947%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A%2218585073516%22%2C%22format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D%7D".format(SongID)
        #获取数据
        data = requests.get(QQAPI).text
        #转换格式
        data:dict = json.loads(data)
        #提取关键参数
        parameter = data["req_0"]["data"]["midurlinfo"][0]["purl"]
        #为空就是下不了
        if parameter == "":
            return None
        #拼接并返回完整下载地址(文件是m4a格式)
        return f"https://isure.stream.qqmusic.qq.com/{parameter}"

    #通用下载函数
    def DownloadFile(self,url:str,Output:str) -> bool:
        """
        通用下载函数
        url:文件链接
        Output:输出路径（包括文件名）
        """
        try:
            res = requests.get(url, headers=self.header)
            if '<!DOCTYPE html>' in str(res.content) :
                print(f"数据获取异常")
                return False
            with open(Output, 'wb') as f:
                f.write(res.content)
            return True
        except Exception as e:
            print(f'出现错误：{e}')
            return False

#读取备份文件
def ReadFile(file:str) -> dict:
    with open(file,encoding='utf-8') as f:
        return json.loads(f.read())



def Main(file:str='listen1_backup.json',OutputPath:str='output') -> None:
    """
    file:Listen1的备份文件地址
    默认为 "listen1_backup.json"
    path:输出文件夹的名称(创建在py文件同目录)
    """
    #从文件读取数据
    Data:dict = ReadFile(file)

    #读取所有歌单编号
    PlaylistID:list = Data['playerlists']

    #从歌单编号获得歌单名
    PlaylistName = []
    for i in PlaylistID:
        PlaylistName.append(Data[i]['info']['title'])

    #添加“当前播放列表”到歌单编号和歌单名列表
    PlaylistID.insert(0,'current-playing')
    PlaylistName.insert(0,'当前播放列表')

    #输出全部歌单
    print(f'文件内共发现{len(PlaylistName)}个歌单')

    for i in range(len(PlaylistName)):
        print(f'[{i}]{PlaylistName[i]} ')

    print('-'*50)

    #询问要下载哪个
    Select = int(input(f'请输入你要下载的歌单序号：'))
    print('-'*50)

    #获取对应歌单的数据
    #Data[PlaylistID[Select]]
    SelectPlaylistData:dict = Data[PlaylistID[Select]]["tracks"]
    SelectPlaylistName:str = Data[PlaylistID[Select]]['info']['title']
    print(f'正在准备下载 {SelectPlaylistName} 中的所有歌曲，共有{len(SelectPlaylistData)}首歌')
    print('-'*50)

    #创建对象
    D = DownloadMusic(OutputPath,SelectPlaylistName)

    #正式开始下载
    #遍历每一首歌的数据
    Done = 0
    Fail = 0
    # for i in range(10):
    for i in range(len(SelectPlaylistData)):
        SongData = SelectPlaylistData[i]
        if D.Download(SongData):
            Done += 1
        else:
            Fail += 1
        print('-'*50)
        # time.sleep(0.5)

    print("歌曲下载完毕")
    print(f"共{len(SelectPlaylistData)}首歌，{Done}首下载成功，{Fail}首下载失败")
    #清理temp目录
    rmtree(D.TempPath)

if __name__ == '__main__':
    Main()