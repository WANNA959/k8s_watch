from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

watchProcess = ["kube-apiserver", "kube-controller-manager", "kube-scheduler", "kube-proxy", "kubelet"]


def check(line):
    for process in watchProcess:
        if process in line:
            return process, True
    return "", False


def check2(line):
    if line.endswith("--\n"):
        return False
    return True


def plot_watch(type, rszDict):
    font = FontProperties(fname='/Users/zhujianxing/Downloads/SimHei.ttf')

    x = range(0, len(rszDict["kube-apiserver"]))
    plt.figure(figsize=(15, 10), dpi=80)
    plt.suptitle("rs变化后3min内内存变化-" + type, fontproperties=font)

    num = 1
    for key in rszDict:
        y = rszDict[key]
        y = list(map(int, y))
        plt.subplot(2, 3, num)
        plt.plot(x, y, label=key)
        num += 1
        plt.xlabel("时间/10s", fontproperties=font)
        plt.ylabel("内存变化/kb", fontproperties=font)
        plt.title(key, fontproperties=font)
        plt.grid(alpha=0.4)
        # plt.legend()

    plt.savefig("./images_v2/" + type + ".png")
    plt.show()


def process_watch_file(filename):
    f = open(filename, "r")
    lines = f.readlines()

    rszDict = dict()
    vszDict = dict()
    for line in lines:
        key, flag = check(line)
        if not flag:
            continue

        if check2(line):
            items = line.split(" ")
            # print(items)
            lens = len(items)
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

    countList = [0, 3]
    for count in countList:
        filename = "./watch_file_v2/watch-" + str(count) + ".txt"
        rszDict, vszDict = process_watch_file(filename)
        plot_watch("rsz-" + str(count), rszDict)
        plot_watch("vsz-" + str(count), vszDict)
