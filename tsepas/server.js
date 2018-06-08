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

app.use(function(req, res, next) { setTimeout(next, 2000)});
// DB connection
var connection = mysql.createConnection({
	host     : 'localhost',
	user     : 'it21633',
	password : '',
	database : 'lib'
});

connection.connect();

app.get('/books/', function(req, res) {
	var title = '%' + req.query.title + '%'; // To a match strings containing the keyword
	connection.query('select * from books where title like ?', [title], function(error, results, fields) {
		if (error) throw error;
		res.send(JSON.stringify(results, null, ' ' ));
	});
});

app.post('/books', function(req, res){
	var author = req.body.author;
	var title = req.body.title;
	var genre = req.body.genre;
	var price = req.body.price;


	connection.on('error', function(err) {
		console.log(err.code); // 'ER_BAD_DB_ERROR'
		res.send("Didn't commit to the database");
	});

	connection.query('INSERT INTO books VALUES(?, ?, ?, ?, ?)', [0, author, title, genre, price], function (error, results, fields) {
		if (error) throw error;
		console.log('The solution is: ', results[0]);
		res.format({
			'text/html': function() {
				res.send('<h1 align=center>All Good</h1>');
			}
		});
	});
});

app.listen(3000, () => console.log('Listening on port 3000..'));

