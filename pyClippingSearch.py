import pytchat
from youtube_transcript_api import YouTubeTranscriptApi

#コメント、配信者の発言から検索したいワードを入力してください。
search_word = "くしゃ"

#archive_list.txtにYoutubeのvideoIDを11文字を記載してください。
#複数を検索に指定する場合は、改行し、1行ごとに入力して下さい(文字コードUTF-8)
with open("archive_list.txt") as file:
    # YouTubeのライブ配信またはプレミアム動画のURLまたは動画IDを設定
    fileName =  "archive_outlist.csv"
    wfile = open(fileName, mode='w', encoding='utf_8')
    lines = file.readlines()
    s_lines = [line.strip() for line in lines]
    for line in s_lines:
        video_id = line
        strurl =  "https://www.youtube.com/watch?v=" + video_id + ","
        #video_id = 'loZAdOr1yPI'
        wfile.write("https://www.youtube.com/watch?v=" + video_id + ",")

        print('============================================================')
        print("https://www.youtube.com/watch?v=" + video_id)
        
        #コメント側
        print('コメント側------------------------------------------------------------')
        #リストの量だけ繰り返す
        commentflag = True
        try:
           chat = pytchat.create(video_id)
        except:
            wfile.write("コメント取得できず,")
            print("コメント取得できず")
            commentflag = False
        if commentflag:
            while chat.is_alive():
                # チャットデータの取得
                chatdata = chat.get()
                for c in chatdata.items:
                    if c.message.find(search_word) >= 0:
                        #print(f"{c.elapsedTime} [{c.author.name}]: {c.message}")
                        wfile.write(f"{c.elapsedTime} [{c.author.name}]: {c.message},")
                        timestmp = c.elapsedTime.split(":")
                        print(timestmp)
                        listLen = len(timestmp)
                        match listLen:
                            case 1:
                                urltime = (int(timestmp[0]) * 1)
                                strurl +=  "https://www.youtube.com/watch?v=" + video_id + r"&t=" + str(urltime) +"s,"

                            case 2:
                                urltime = (int(timestmp[0]) * 60) + (int(timestmp[1]) * 1)
                                strurl +=  "https://www.youtube.com/watch?v=" + video_id + r"&t="  + str(urltime) +"s,"

                            case 3:
                                urltime = (int(timestmp[0]) * 60 * 60) + (int(timestmp[1]) * 60) + (int(timestmp[2]) * 1)
                                strurl +=  "https://www.youtube.com/watch?v=" + video_id + r"&t="  + str(urltime) +"s,"
                                #print((int(timestmp[0]) * 60 * 60))
                                #print(int(timestmp[1]) * 60)
                                #print(int(timestmp[2]) * 1)

                            case _:
                                strurl +=  "変換なし,"

        subscribeflag = True
        #字幕側
        print('字幕側------------------------------------------------------------')
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        except:
            wfile.write("字幕取得できず,")
            print("字幕取得できず")
            subscribeflag = False

        if subscribeflag:
            for transcript in transcript_list:
                for tr in transcript.fetch():
                    if str(tr['text']).find(search_word) >= 0:
                        sec = tr['start']
                        print(sec)
                        hour = int(sec / 3600) 
                        minutes = int((sec % 3600) / 60)
                        second = int(sec - (hour * 3600) - (minutes * 60))
                        time = str(hour) + ':' + str(minutes) + ':' + str(second)
                        outputTxt = time + ' ' + str(tr['text'])
                        #print(outputTxt)
                        wfile.write(outputTxt + ",")
                        strurl +=  "https://www.youtube.com/watch?v=" + video_id + r"&t="  + str(int(sec)) +"s,"
        #print(strurl)
        wfile.write("\n")
        wfile.write(strurl)
        wfile.write("\n")
    wfile.close()

