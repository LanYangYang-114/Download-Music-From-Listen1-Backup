# Download-Music-From-Listen1-Backup

批量下载Listen1歌单备份文件中的所有音乐

代码写的不咋地，第一次在github上传代码，没准有人需要吧

# 关于本程序

本程序可以自动下载歌单中的音乐为mp3文件，并给文件添加封面和歌手等信息，可在各类音乐播放器中正常显示信息，只支持windows，需要在linux用可以自行修改

![image](https://github.com/LanYangYang-114/Download-Music-From-Listen1-Backup/assets/84030410/27ca094f-cc51-442f-9de8-060cd570752f)

本程序并不能下载付费音乐，只能下载可免费收听的音乐，音质最高128kbps(没找到下载更高音质的方法)，想要高音质和需要付费的音乐建议使用官方音乐客户端

目前只支持下载歌单中来自网易云音乐和QQ音乐的曲目，其他平台还不会搞

做这个程序的原因是学校教学楼的公用网络内没法使用Listen1听来自网易云音乐的歌，但我的歌单中绝大部分都来自网易云音乐，尝试各种办法无效，一不做二不休，直接全部下载下来到本地听，完美解决这个问题

# 使用方法
确保你的python环境中包含request库，并额外下载ffmpeg到你的电脑上

在Listen1设置中备份(导出)你的歌单

![image](https://github.com/LanYangYang-114/Download-Music-From-Listen1-Backup/assets/84030410/de89d491-0752-4e63-bca9-2e8dc1b1d189)

将备份出的歌单文件放在该程序同一目录下

![image](https://github.com/LanYangYang-114/Download-Music-From-Listen1-Backup/assets/84030410/e471c1c0-6385-48ff-8e2e-f4647dd830aa)

如果你修改了歌单备份文件的文件名，你需要在程序最后手动添加文件名

![image](https://github.com/LanYangYang-114/Download-Music-From-Listen1-Backup/assets/84030410/f43a373e-ecbb-4d30-8be2-3e989970fe0f)

如果你想输出到指定目录，你可以手动指定输出目录(默认使用output)，输出文件夹会创建在程序目录下

![image](https://github.com/LanYangYang-114/Download-Music-From-Listen1-Backup/assets/84030410/90f89eaf-dcd4-4984-a9c7-475b3098e1ff)

将ffmpeg.exe复制到该程序同一目录下

![image](https://github.com/LanYangYang-114/Download-Music-From-Listen1-Backup/assets/84030410/555fa8e3-1e57-4ec5-a6a0-4456fd841b5f)

完成上述步骤后，运行main.py即可开始下载音乐

![image](https://github.com/LanYangYang-114/Download-Music-From-Listen1-Backup/assets/84030410/4341bbe9-6aa1-4962-9f25-7d5e8d253c12)

![image](https://github.com/LanYangYang-114/Download-Music-From-Listen1-Backup/assets/84030410/a3255cc2-f46d-40e6-992c-715ba37d95c5)
