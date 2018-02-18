try:
    file_1 = open("test1.txt", "w")
    print("Writing into a file...")
    file_1.write("Hello, Worlrsd!")
    file_1.close()
except:
    print("Error happened!")
