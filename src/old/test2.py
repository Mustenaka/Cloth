import test


# 创建新线程
thread1 = test.myThread(1, "Thread-1", 1)
thread2 = test.myThread(2, "Thread-2", 2)

# 开启新线程
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print ("退出主线程")