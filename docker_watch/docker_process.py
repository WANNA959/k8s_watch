from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties


def check(line):
    if line.endswith("--\n"):
        return False
    return True


def plot_watch(memoryList):
    font = FontProperties(fname='../SimHei.ttf')

    # 指定大小 dpi指定每英寸像素点，越大越清晰
    plt.figure(figsize=(20, 8), dpi=80)
    plt.title("docker启动1min内存变化" , fontproperties=font)

    x=range(len(memoryList))
    plt.plot(x, memoryList)

    plt.xlabel("时间/s", fontproperties=font)
    plt.ylabel("内存变化/mb", fontproperties=font)

    plt.grid(alpha=0.4)

    plt.savefig("./docker-memory.png")
    plt.show()


def process_watch_file(filename):
    f = open(filename, "r")
    lines = f.readlines()

    memoryList = []
    for line in lines:
        if not check(line):
            continue
        line=line.strip('\n')
        line=line.strip('M')
        memoryList.append(int(line))
    return memoryList


if __name__ == '__main__':

    filename = "./memory-change.txt"
    memoryList = process_watch_file(filename)
    print(memoryList)
    plot_watch(memoryList)
