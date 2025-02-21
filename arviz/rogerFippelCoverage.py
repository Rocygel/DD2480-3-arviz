def main():
    branchesVisited = [False] * 1000

    file = open("pairplot_coverage.txt", "r")
    for line in file:
        branchesVisited.append(line)
        branchesVisited[int(line)] = True

    file.close()

    file = open("pairplot_coverage.txt", "w")

    for i in range (1, len(branchesVisited)):
        if branchesVisited[i] == True:
            file.write(f"{i}\n")

if __name__ == "__main__":
    main()



