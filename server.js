const express = require('express');
const path = require('path');
const fs = require ("fs")
const app = express();
const PORT = 8080; // You can change the port if needed
const cors = require('cors');
app.use(express.static('files'));
// Disable CORS
app.use(cors());

app.get('/', (req, res) => {
    fs.readdir("./files", (err, files) => {
      if (err) {
        console.error('Error reading directory:', err);
        res.status(500).send('Internal Server Error');
        return;
      }
      // Render the list of files as an HTML page
      const fileList = files.map(file => `<a href="/${file}" target="_blank">${file}</a><br />`).join('');
      const html = `<h1>Files in the Directory:</h1><ul>${fileList}</ul>`;
      res.send(html);
    });
  });
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});