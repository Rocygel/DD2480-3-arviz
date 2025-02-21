#helper script for essplot manual branch cover check


# '2', '5', '8', 7, 6]

def calculate_coverage(coverage_array):


    statments = {
    "1": 2,  "2": 2,  "3": 2,  "4": 2,  "5": 2,  
    "6": 2,  "7": 5,  "8": 5,  "9": 7,  "10": 3,  
    "11": 2
    }

    with open("essplot_coverage.txt", "r") as file:
            lines = []
            for line in file:
                    clean_line = line.strip() 
                    if not clean_line.startswith("coverage:"):  # Skip lines that start with "coverage"
                            lines.append(clean_line)

    # Get unique elements by using the symmetric difference (XOR)
    unique_branches = list(set(coverage_array + lines))
    print(unique_branches)

    ran_branches = 0
    for branch in unique_branches:
            nr_of_statments = statments[branch]
            ran_branches += nr_of_statments

    missing = 34 - ran_branches

    coverage = (74-missing)/74
    print(str(coverage*100)+"% \n")

    with open("essplot_coverage.txt", "w") as file:
            for branch in unique_branches:
                    file.write(str(branch)+"\n")
            file.write("coverage: "+ str(coverage*100)+"% \n")