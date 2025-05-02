# Settings
INPUT_DATA_FILEPATH = r"html\Table Basics\Final assessment\data.txt"
OUTPUT_HTML_PARTIAL_FILEPATH = r"html\Table Basics\Final assessment\partial.html"
####

# Troubleshooting
#   If your relative file-paths don't work, make a virtual environment, and 
#       .. check os.listdir() to find the working directory
####

def generateTagsFromData(input_f: str, output_f: str) -> None:
    """Populates an output file with html tags according to the
       space-separated-value input data.
       
        Arguments:
            output_f (str): A relative path of where the output file should be created.
            input_f (str): A relative path pointing to the input data file
        
        Returns:
            None
            
        Data Input:
            header 0.0 0.0 0.0 0.0 0.0 0.0 (optional) String of words
        Data Output:
            <th>header</th><td>0.0</td> ... <td>String of words</td>
    """
       
    data_values: list # Typed unassigned variable

    with open(input_f, 'r') as in_obj:
        with open(output_f, 'w') as out_obj:
            for line in in_obj.readlines():
                data_values = line.split(" ") # Split along " "
                
                header = data_values[0]       # Grab header
                floats = data_values[1:9]     # Grab data floats
                end_string = data_values[9:]  # Grab end string words (notes field)
                
                # Write to partial file
                out_obj.write("<tr>\n")
                out_obj.write(f"\t<th>{header}</th>\n")
                for data in floats:
                    out_obj.write(f"\t<td>{data.rstrip()}</td>\n") # .rstrip() removes existing line-ending
                    
                # If there is a string, ...
                if len(end_string) != 0:
                    joined_str = ' '.join(end_string).rstrip() # ... join word list with space deliminator.
                    out_obj.write(f"\t<td>{joined_str}</td>\n")
                out_obj.write("</tr>\n")

    print("Generated HTML output!")


def main() -> None:
    #print(os.listdir())
    generateTagsFromData(INPUT_DATA_FILEPATH, OUTPUT_HTML_PARTIAL_FILEPATH) 


if __name__ == "__main__":
    main()
