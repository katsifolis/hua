// Simple http server

var express = require('express');
var app = express();
var serveStatic = require('serve-static');

app.use(serveStatic('./', {'index': ['index.html', 'default.htm']}))

app.listen(8081);

// Simple mySQL server
var mysql      = require('mysql');

var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '',
  database : 'test'
});
 
connection.connect();

connection.query('SELECT * FROM workers', function (error, results, fields) {
  if (error) throw error;
	console.log('The solution is: ', results[0]);
});
