// Simple http server

var express = require('express');
var app = express();
var serveStatic = require('serve-static');

app.use(serveStatic('./', {'index': ['index.html', 'default.htm']}))

app.listen(8081);
