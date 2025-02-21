import ast  # To safely convert string representation of lists into actual lists

def main():
    combined_coverage = None  # This will store the final cumulative list

    # Read and process the coverage file
    with open("coverage.txt", "r") as file:
        for line in file:
            try:
                branch_list = ast.literal_eval(line.strip())  # Convert string to list
                
                if combined_coverage is None:
                    combined_coverage = branch_list[:]  # Initialize with first list
                else:
                    # Perform an element-wise OR operation
                    combined_coverage = [a or b for a, b in zip(combined_coverage, branch_list)]
            
            except (SyntaxError, ValueError):
                print(f"Skipping invalid line: {line.strip()}")  # Handle malformed lines

    tot_true= sum(combined_coverage)
    total_length = len(combined_coverage)
    tot_Cov = round((tot_true/total_length)*100)
    # Write the final combined list to a new file
    with open("combined_coverage.txt", "w") as file:
        file.write(str(combined_coverage) + "\n")  # Save as a single list
        file.write(str(tot_Cov)+"%\n")

if __name__ == "__main__":
    main()
