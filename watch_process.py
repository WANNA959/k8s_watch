from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties


def check(line):
    if line.endswith("--\n"):
        return False
    return True


def plot_watch(type, rszDict):
    font = FontProperties(fname='/Users/zhujianxing/Downloads/SimHei.ttf')

    x = range(0, len(rszDict["10530"]))
    plt.figure(figsize=(15, 10), dpi=80)
    plt.suptitle("rs变化后3min内内存变化-" + type, fontproperties=font)
    labelDict = {
        "10530": "apiserver",
        "10736": "kubelet",
        "10451": "controller",
        "10540": "scheduler",
        "11166": "proxy"
    }

    num = 1
    for key in labelDict:
        y = rszDict[key]
        y = list(map(int, y))
        plt.subplot(2, 3, num)
        plt.plot(x, y, label=labelDict[key])
        num += 1
        plt.xlabel("时间/10s", fontproperties=font)
        plt.ylabel("内存变化/kb", fontproperties=font)
        plt.title(labelDict[key], fontproperties=font)
        plt.grid(alpha=0.4)
        # plt.legend()

    plt.savefig("./images/" + type + ".png")
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

    countList = [0, 3, 10, 20, 30, 40]
    for count in countList:
        filename = "./watch_file/watch-" + str(count) + ".txt"
        rszDict, vszDict = process_watch_file(filename)
        plot_watch("rsz-" + str(count), rszDict)
        plot_watch("vsz-" + str(count), vszDict)
