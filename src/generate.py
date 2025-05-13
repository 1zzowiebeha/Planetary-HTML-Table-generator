import os

############
# Settings #
############

INPUT_DATA_FILENAME = "data.txt"
OUTPUT_DIR = "public"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_PATH = os.path.join(BASE_DIR, OUTPUT_DIR)
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

INPUT_DATA_PATH = os.path.join(BASE_DIR, INPUT_DATA_FILENAME)

####################
# Troubleshooting: #
####################
#   If your relative file-paths don't work, make a virtual environment, and 
#       .. check os.listdir() to find the working directory
####################

class Template:
    """A static HTML page with dynamic data insertion capability."""
    def __init__(self, template_path: str):
        self.template_path = template_path
        
        self.fullname = os.path.basename(template_path)

    def get_contents(self) -> str:
        """Return the HTML contents of a template file as a string."""
        with open(self.template_path, 'r') as file_object:
            return file_object.read()

    def render(self, context_data: dict[str, str]) -> str:
        """Populate a template's unfilled variables with context data."""
        html_contents = self.get_contents()
        
        return html_contents.format(**context_data)


def minify(html_contents: str) -> str:
    """Remove newlines from the HTML"""
    # todo
    return html_contents


def get_template(template_name: str) -> Template | None:
    """Return the path to the passed template as a string.
    Will recursively search the templates dir until the first occurence of
    <template_name>.html is found."""
    
    template_file_name = f"{template_name}.html"
    
    for root, dirs, files in os.walk(TEMPLATES_DIR):
        if template_file_name in files:
            return Template(os.path.join(root, template_file_name))
    
    return None

def generateTableBody(data_filepath: str) -> str:
    """Produces table body tags from a data file.
            
        Data Input:
            header 0.0 0.0 0.0 0.0 0.0 0.0 (optional) String of words
        Data Output:
            <th>header</th><td>0.0</td> ... <td>String of words</td>
    """
       
    data_values: list # Typed unassigned variable
    data_string = ""

    with open(data_filepath, 'r') as in_obj:
        for line in in_obj.readlines():
            data_values = line.split(" ") # Split along " "
            
            header = data_values[0]       # Grab header
            floats = data_values[1:9]     # Grab data floats
            end_string = data_values[9:]  # Grab end string words (notes field)
            
            # Write to partial file
            data_string += ("<tr>\n")
            data_string += f"\t<th>{header}</th>\n"
            for data in floats:
                data_string += f"\t<td>{data.rstrip()}</td>\n" # .rstrip() removes existing line-ending
                
            # If there is a string, ...
            if len(end_string) != 0:
                joined_str = ' '.join(end_string).rstrip() # ... join word list with space deliminator.
                data_string += f"\t<td>{joined_str}</td>\n"
            data_string += "</tr>\n"


def publish_tabular_data():
    """Generate, render, and output planetary data
    into a viewable HTML file."""
    
    # bug: Protect against XSS
    table_body = generateTableBody(INPUT_DATA_PATH)
    
    context = {
        "table_body": table_body
    }
    
    template = get_template("data_visualized")
    
    rendered_html = template.render(context)
    
    minified_html = minify(rendered_html)
    
    output_filepath = os.join(OUTPUT_PATH, template.fullname)
    with open(output_filepath, "w") as file_object:
        file_object.write(minified_html)
        

def main() -> None:
    """Entry point of the program."""
    publish_tabular_data() 


if __name__ == "__main__":
    main()