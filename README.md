# Planetary-HTML-Table-generator

## Input data file:

![image](https://github.com/user-attachments/assets/77ffec5d-baf4-41f7-af5b-c2c780caea04)

## Output HTML:

![firefox_qx1SRvyEsu](https://github.com/user-attachments/assets/47d0f2d3-1f98-4b18-8392-62c7c035dbe8)

## About:

Adapted from MDN's [accessible table example](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Planet_data_table).

Takes a data file containing planetary data such as name, mass, density, distance from the sun, etc.
and converts it into a highly semantic HTML table for data visualization.

## Development

### 0. Generate HTML from data.txt

To generate the full HTML page in /public/, run

`python generate.py`

### 1. Install Dart Sass executable through NPM
`npm -i global install sass-embedded`

### 2. Compile SASS to CSS in real-time

From repository's root dir:

`sass --watch src/styles:public/styles`

 ❗Note: `/src/styles/` file deletions may not reflect in `/public/styles/`
use a build tool or NPM scripts for a better watch mechanism

### 3. Live CSS updates in the browser

Use a LiveServer mechanism like VSCode's LiveServer to view your changes in real-time