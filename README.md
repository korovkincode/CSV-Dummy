<h1>CSV-Dummy</h1>
<h3>CSV-Dummy is an online service for generating CSV files with fake data</h3>
<h4>Features:</h4>
<ul>
<li>Any logged-in user can create any number of data schemas to create
datasets with fake data.</li>
<li>Each such data schema has a name and a list of columns with names and
specified data types.</li>
<li>There are 5 different types of data (soon it will be more):
<ul>
<li>Full name</li>
<li>Job</li>
<li>Domain name</li>
<li>Company name</li>
<li>Address</li>
</ul>
<li>Users can build the data schema with any number of columns of any type
described above.</li>
<li>Each column also has its own name (which will be a column header in the
CSV file) and order (just a number to manage column order).</li>
<li>After creating the schema, the user should be able to input the number of
records he/she needs to generate and press the “Generate data” button.</li>
<li>After pressing the button, the frontend sends an AJAX request to
the server to generate the data. When the CSV file of the specified
structure is ready, the file can be saved to the “media” directory.</li>
<li>The interface shows a colored label of generation status for each
dataset (processing/ready).</li>
<li>Desing mockup - <a href="https://www.figma.com/file/GLah5wCMHIyw7hJI4Gekns/CSV-fake-data-generator?node-id=24278%3A2">here</a></li>
</ul>
<h3>Technology Stack</h3>
<ul>
<li>Python 3</li>
<li>Django</li>
<li>Faker</li>
<li>Bootstrap</li>
</ul>
<p>Project requirements are in requirements.txt</p>