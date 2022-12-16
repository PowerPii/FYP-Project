const mysql = require('mysql2');

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '128bitslonger',
    port: 3306
  });
  
  connection.connect(error => {
    if (error) {throw error}
    console.log('Connected to the database successfully');
  });

module.exports = connection;