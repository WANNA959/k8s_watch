from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties


def check(line):
    if line.endswith("--\n"):
        return False
    return True


def plot_watch(type, rszDict,vszDict):
    font = FontProperties(fname='./SimHei.ttf')

    x = range(0, len(rszDict["10530"]))
    # 指定大小 dpi指定每英寸像素点，越大越清晰
    plt.figure(figsize=(20, 8), dpi=80)
    plt.suptitle("rs变化后100s内内存变化-" + type, fontproperties=font)
    labelDict = {
        "10530": "apiserver",
        "10736": "kubelet",
        "10451": "controller",
        "10540": "scheduler",
        "11166": "proxy"
    }

    key = "10530"
    y1 = list(map(int, rszDict[key]))
    y2 = list(map(int, vszDict[key]))
    num=1
    for y in [y1,y2]:
        plt.subplot(1,2,num)
        num+=1
        plt.plot(x, y, label=labelDict[key] + "-" + type)

        plt.xlabel("时间/5s", fontproperties=font)
        plt.ylabel("内存变化/kb", fontproperties=font)
        title="rsz" if num ==2 else "vsz"
        plt.title(title, fontproperties=font)
        plt.grid(alpha=0.4)

    plt.savefig("./api_images/" + type + ".png")
    plt.show()


def process_watch_file(filename):
    f = open(filename, "r")
    lines = f.readlines()

    rszDict = dict()
    vszDict = dict()
    for line in lines:
        if check(line):
            items = line.split(" ")
            # print(items)
            lens = len(items)
            key = ""
            for key in items:
                if len(key) != 0:
                    break
            memset = rszDict.get(key)
            if memset == None:
                memset = list()
            memset.append(items[lens - 3])
            rszDict[key] = memset

            memset = vszDict.get(key)
            if memset == None:
                memset = list()
            memset.append(items[lens - 2])
            vszDict[key] = memset
    return rszDict, vszDict


if __name__ == '__main__':

    countList = [10, 20, 30, 40]
    for count in countList:
        filename = "./api_data_file/api-" + str(count) + ".txt"
        rszDict, vszDict = process_watch_file(filename)
        plot_watch(str(count), rszDict,vszDict)
