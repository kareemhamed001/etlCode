import os
from queue import Queue
from VideoProducer import VideoProducer
from VideoConsumer import VideoConsumer
from ExcelWriter import ExcelWriter

if __name__ == "__main__":
    def ExcelSheetGenerator(columnList,video_Path,sheet_path,model_Path,folder_path):
    
        video_name=os.path.splitext(os.path.basename(video_Path))[0] 

        sheet = r"{}\{}.xlsx".format(sheet_path, video_name)

        q = Queue()
        ExcelQ = Queue()
        DependcisQ = Queue()
        shape = (128, 128)

        folder_list = []

        for folder in os.listdir(folder_path):
            if os.path.isdir(os.path.join(folder_path, folder)):
                folder_list.append(folder)
            else:
                print("Incorrect Path !!")

        classes = folder_list

        P = VideoProducer(q, DependcisQ, video_Path, model_Path, classes, shape)
        C = VideoConsumer(q, DependcisQ, ExcelQ)
        W = ExcelWriter(ExcelQ, sheet,columnList)
        P.start()
        C.start()
        W.start()

        P.join()
        C.join()
        W.join()
