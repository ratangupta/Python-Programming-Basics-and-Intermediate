# Introduction to Multiprocessing 

from multiprocessing import Process, Pool

# barca = (["Messi is the best player in the world."],
#         ["Xavi and Iniesta are the best midfielders in the world."],
#         ["Puyol is the best defender in the world."],
#         ["Pique best represents the club."],
#         ["Neymar is the best showboater in the club."])

def out(num):
    print("https://www.python.org {}".format(num))

# def forca_barca(item):
#     print("{}".format(item))

if __name__ == '__main__':
    for i in range(5):
        p = Process(target = out, args = (i,))
        p.start()
        p.join()

# def job(num):
#     return num * 2

# if __name__ == '__main__':
#     p = Pool(processes=20)
#     data = p.map(job, range(20))
#     p.close()
#     print(data)