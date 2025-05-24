import os
import warnings
from typing import Self

############
# Settings #
############

# A single "\" at the end of a docstring line
# ... will ignore its implicit newline.

WELCOME_MESSAGE = """
#################################
    Planetary HTML Table Generator
#################################
"""

INPUT_DATA_FILENAME = "data.txt"
OUTPUT_DIR = "public"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
INPUT_DATA_PATH = os.path.join(BASE_DIR, INPUT_DATA_FILENAME)

ROOT_DIR = os.path.join(BASE_DIR, "..")
OUTPUT_PATH = os.path.join(ROOT_DIR, OUTPUT_DIR)

############

class TemplateNotFoundException(Exception):
    pass


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
        """Populate a template's unfilled format variables with context data."""
        html_contents = self.get_contents()
        
        return html_contents.format(**context_data)

    # If we create subclasses from this Template,
    # ... we may need a get_template() mixin to properly annotate
    # ... the cls type as Template.
    @classmethod
    def get_template(cls: Self, template_name: str) -> Self:
        """Return a template class created via the passed template name.
        Recursively searches the /src/templates/ dir until the first occurence of
        <template_name>.html is found. Will raise an error if nothing is found."""
        
        template_file_name = f"{template_name}.html"
        
        for root, dirs, files in os.walk(TEMPLATES_DIR):
            if template_file_name in files:
                return cls(os.path.join(root, template_file_name))
        
        raise TemplateNotFoundException(f"Could not find template {template_name} in src/templates/")


def minify(html_contents: str) -> str:
    """Remove whitespace and newlines from the HTML."""
    warnings.warn("Minification is yet to be implemented.")
    
    return html_contents


def generateTableBody(data_filepath: str) -> str:
    """Produce a string of <th> and <td> tags from the passed data file.
    
        Expects the data input file to positionally contain:
            1 header string, 8 floats, and an optional string of space-separated words.
        
        Data Input:
            header 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 [optional: Space-separated words]
        Data Output:
            <th>header</th><td>0.0</td> ... <td>A string of words</td>
    """
       
    tbody_contents = ""

    with open(data_filepath, 'r') as file_object:
        for line in file_object.readlines():
            data_values: list[str] = line.split(" ")
            
            header: str = data_values[0]             # Grab table header
            floats: list[str] = data_values[1:9]     # Grab the 8 data floats
            end_string: list[str] = data_values[9:]  # Grab end string words (notes field)
            
            # Write to HTML partial buffer
            tbody_contents += ("<tr>\n")
            tbody_contents += f"\t<th>{header}</th>\n"
            for datum in floats:
                # .rstrip() removes the implicit newline
                tbody_contents += f"\t<td>{datum.rstrip()}</td>\n"
            
            # If there are words within the notes field list:
            if len(end_string) != 0:
                # Join word list with space deliminator.
                joined_str = ' '.join(end_string).rstrip()
                tbody_contents += f"\t<td>{joined_str}</td>\n"
            tbody_contents += "</tr>\n"
    
    if not tbody_contents:
        raise Exception("No data present in file supplied.")
    
    return tbody_contents


def publish_tabular_data():
    """Generate, render, and write planetary data
    to an HTML file under /public/."""
    
    table_body: str = generateTableBody(INPUT_DATA_PATH)
    
    context = {
        "table_body": table_body
    }
    
    template: Template = Template.get_template("data_visualized")
    rendered_html: str = template.render(context)
    minified_html: str = minify(rendered_html)
    
    output_filepath: str = os.path.join(OUTPUT_PATH, template.fullname)
    with open(output_filepath, "w") as file_object:
        file_object.write(minified_html)
        

if __name__ == "__main__":
    print(WELCOME_MESSAGE)
    print("Publishing to /public/...\n")
    
    publish_tabular_data() 

    print("\nFinished.")