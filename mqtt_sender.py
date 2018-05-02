import threading
import time
import subprocess
# 完全原生强制结束python线程的方法。转载请注明来自博客园


def func(tHandle, timeout):
    # caller 函数
    print('in time control.')
    tHandle.setDaemon(True)  # 设置tHandle线程为daemon,关键地方！！
    tHandle.start()  # 让tHandle线程进入阻塞状态
    tHandle.join(10)  # tHandle 有timeout这么多秒的时间运行之后进入阻塞（也可以认为是挂起）

    print('out time control')  # 这句执行完毕后，由于tHandle线程是此线程的守护程序
    # 因此caller结束后tHandle也就结束了，从而达到kill tHandle线程的目的


def checkproxy(timewait, timewait2):
    print('in checkproxy.')
    subprocess.call(['notepad'])
    print('out checkproxy.')  # 这句在此例子里是不运行的，因为此句要在20+1=21秒之后运行，
    # 但是caller 只给了2秒时间运行，然后caller结束，此线程也要结束。所以运行不到


tcheck = threading.Thread(target=checkproxy, args=(1, 20,))
caller = threading.Thread(target=func, args=(tcheck, 8,))


caller.start()
input()
