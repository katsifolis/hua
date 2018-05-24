'use strict';
var book = {
	author: "",
	title: "",
	genre: "",
	price: 20

}

function Book(author, title, genre, price) {
	this.author = author;
	this.title = title;
	this.genre = genre;
	this.price = price;

}

var tAuthor = document.getElementById('author').value;
var tTitle = document.getElementById('title').value;
var tGenre = document.getElementById('genre').value;
var tPrice = document.getElementById('price').value;

var b = new Book(tAuthor, tTitle, tGenre, tPrice);


document.getElementById('but').addEventListener('click', () => alert(JSON.stringify(b)));

//document.getElementById('author')
//function ask(question, yes, no) {
//  confirm(question)
//	 ? yes() : no()
//  
//}
//
//ask(
//  "Do you agree?",
//  () => alert('You agreed'),
//  () => alert('You agreedn\'t')
//);


let user = {
	name: "John",
	lastName: "Doe",
	sayHi() {
		console.log('Hey');
		let sayBye = () => console.log('Bye');
	}
};

function User(name, lastName) {
	this.name = name;
	this.lastName = lastName;
}

