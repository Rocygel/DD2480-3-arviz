def main():
    branchesVisited = [False] * 1000

    print("Hello, this is the main function!")
    file = open("testfile.txt", "r")
    for line in file:
        branchesVisited.append(line)
        branchesVisited[int(line)] = True

    file.close()

    file = open("testfile.txt", "w")

    for i in range (1, len(branchesVisited)):
        if branchesVisited[i] == True:
            file.write(f"{i}\n")

if __name__ == "__main__":
    main()



