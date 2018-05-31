'use strict';
// Simple http server

var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var mysql = require('mysql');
// For serving static files

app.use(express.static('./'));


// For parsing the Json Objects

app.use(bodyParser.json());

app.use(bodyParser.urlencoded({ extended: false }));

// DB connection
var connection = mysql.createConnection({
	host     : 'localhost',
	user     : 'root',
	password : '04215mom',
	database : 'lib'
});

app.get('/books/:id', function(req, res) {
	res.send(req.params);
});

app.post('/books', function(req, res){
	var author = req.body.author;
	var title = req.body.title;
	var genre = req.body.genre;
	var price = req.body.price;

	connection.connect();

	connection.on('error', function(err) {
		console.log(err.code); // 'ER_BAD_DB_ERROR'
	});


//connection.query('select max(id) from books', function (error, results, fields) {
//
//	console.log(results[0]);
//	console.log(results.insertId);
//
//});



	connection.query('INSERT INTO books VALUES(?, ?, ?, ?, ?)', [0, author, title, genre, price], function (error, results, fields) {
		if (error) throw error;
		console.log('The solution is: ', results[0]);
	});
});

app.listen(8081, () => console.log('Listening on port 8081'));

