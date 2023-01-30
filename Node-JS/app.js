var bodyParser = require('body-parser');
const crypto = require('crypto');
const express = require('express');
const mysql = require('mysql2');
const nodemailer = require('nodemailer');
const rateLimit = require('express-rate-limit');
const session = require('express-session');

const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, 
    max: 5, 
    message: 'Too many login attempts from this IP, please try again later'
});

const app = express();
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(session({secret: "hi", resave: true, saveUninitialized: true}));

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


// ----------------------------------- //

// TELEGRAM ONLY

// Handle GET requests

app.get('/admin/get', (req, res) => {
    const {request, database} = req.query;

    if (request == "ALL") {
        connection.query(`SELECT * FROM application.${database}`, (error, results) => {
            if (error) {throw error}
            res.send(results);
        });
    }
    else {
        res.sendStatus(404);
    }
});
    
// Handle POST request

app.post('/admin/post', (req, res) => {
    const {request, database, data} = req.body;

    if (request == "APPEND") {
        if (database == "risks") {
            let date = data.date;
            let time = data.time;
            let risks = JSON.stringify(data.risks).replaceAll('"', '\'')

            query = `INSERT INTO application.${database} VALUES ("${date}", "${time}", ${JSON.stringify(risks)})`
            connection.query(query, (error, results) => {if (error) {throw error}})
            res.send("Data appended succesfully")
        }
        else if (database == "bus_arrival") {
            const {date, time, service_no, arrival_time, latitude, longitude} = data;
            query = `INSERT INTO application.${database} VALUES ("${date}", "${time}", "${service_no}",  "[${arrival_time}]",  "[${latitude}]", "[${longitude}]")`
            connection.query(query, (error, results) => {if (error) {throw error}})
            res.send("Data appended successfully")
        }
    }
    else if (request == "DELETE") {
        query = `DELETE FROM application.${database}`
        connection.query(query, (error, results) => {if (error) {throw error}})
        res.send("Data deleted succesfully")
    }
    else {
        res.sendStatus(404);
    }
});

// ----------------------------------- //

// WEBSITE

// HOMEPAGE PAGE

app.get('/', (req, res) => {
    is_login = req.session.authenticated
    username = "username" in req.session ? req.session.username : null;

    res.render('homepage', {is_login, username})
});

// PROFILE PAGE

app.get('/profile', (req, res) => {
    req.session.is_otp = false;
    req.session.otp = null;

    is_login = req.session.authenticated
    username = req.session.username
    email = req.session.email

    res.render('profile', {is_login, username, email})
});

app.post('/profile', (req, res) => {
    res.redirect('/reset-password');
});

// SIGN UP PAGE

app.get('/signup', (req, res) => {
    req.session.is_otp = false;
    req.session.otp = null;
    req.session.email = null;

    res.render('signup');
});

app.post('/signup', (req, res) => {
    const {email, username, password, confirmed_password} = req.body;
    if (password == confirmed_password) {
        query = `SELECT * FROM application.users WHERE Username = "${email}"`;
        connection.query(query, (error, results) => {
            if (error) {throw error}
            if (results.length == 0) {
                query = `SELECT * FROM application.users WHERE Username = "${username}"`;
                connection.query(query, (error, results) => {
                    if (error) {throw error}
                    if (results.length == 0) {
                        query = `INSERT INTO application.users VALUES ("${email}", "${username}", "${password}")`;
                        connection.query(query, (error, results) => {
                        if (error) {throw error}
                        
                        let transporter = nodemailer.createTransport({host: 'smtp.gmail.com', port: 465, secure: true, auth: {user: 'hashthe13@gmail.com', pass: 'hopjdkrlljqeduyy'}});
                        transporter.sendMail({from: '"ReRAC" <hashthe13@gmail.com>', to: email, subject :"Welcome to ReRAC", text: `Hi, ${username}.\n\nYour registration to ReRAC is successful!\n\nCheers,\nReRAC Teams`});

                        res.redirect("/login");
                        });
                    }   
                    else {res.redirect('/signup')}
                });
            } 
            else {res.redirect('/signup');}
        });
    }
    else {res.redirect('/signup');}
});

// LOGIN PAGE

app.get('/login', (req, res) => {
    req.session.is_otp = false;
    req.session.otp = null;
    req.session.email = null;

    res.render('login')
});

app.post('/login', (req, res) => {
    const {username, password} = req.body;
    query = `SELECT * FROM application.users WHERE Username = "${username}" OR Email = "${username}"`;
    connection.query(query, (error, results) => {
        if (error) {throw error}
        if (results.length != 0) {
            if (password == results[0].Password) {
                req.session.authenticated = true;
                req.session.email = results[0].Email;
                req.session.username = results[0].Username;
                req.session.password = password;
                res.redirect('/profile');
            } else {res.redirect('/login');}
        } else {res.redirect('/login');}
    });
});

// LOGOUT

app.get('/logout', (req, res) => {
    req.session.authenticated = false;
    req.session.email = null;
    req.session.username = null;
    req.session.password = null;
    res.redirect("/");
});

// FORGOT PASSWORD

app.get('/forgot-password', (req, res) => {
    is_otp = "is_otp" in req.session ? req.session.is_otp : false;
    res.render('forgot-password', {is_otp});
});

app.post('/forgot-password', (req, res) => {
    const email = "email" in req.body ? req.body.email : null;
    const otp = "otp" in req.body ? req.body.otp : null;
    const is_otp = "is_otp" in req.session ? req.session.is_otp : false;

    if (is_otp) {
        req.session.is_otp = false;
        if (otp == req.session.otp) {res.redirect('/reset-password');}
        else {res.redirect('/forgot-password');}
    }
    else {
        if (email != null) {
            query = `SELECT * FROM application.users WHERE Email = "${email}"`;
            connection.query(query, (error, results) => {
                if (error) {throw error}
                if (results.length != 0) {
                    const buffer = crypto.randomBytes(3);
                    const otp = buffer.toString('hex').toUpperCase();
                    
                    req.session.is_otp = true;
                    req.session.email = email;
                    req.session.otp = otp;
    
                    let transporter = nodemailer.createTransport({host: 'smtp.gmail.com', port: 465, secure: true, auth: {user: 'hashthe13@gmail.com', pass: 'hopjdkrlljqeduyy'}});
                    transporter.sendMail({from: '"ReRAC" <hashthe13@gmail.com>', to: email, subject :"ReRAC Password Reset OTP", text: `Hi ${username}Enter the OTP below to reset your password\n\n${otp}\n\nCheers,\nReRAC Teams`});
                }
                res.redirect('/forgot-password');
            });
        }
    }
});

// RESET PASSWORD

app.get('/reset-password', (req, res) => {
    req.session.otp = null;
    is_login = req.session.authenticated;
    res.render('reset-password', {is_login});
});

app.post('/reset-password', (req, res) => {
    const {new_password, confirmed_password} = req.body;
    const email = req.session.email;
    if (new_password == confirmed_password) {
        query = `UPDATE application.users SET Password = "${new_password}" WHERE Email = "${email}"`;
        connection.query(query, (error, results) => {
            let transporter = nodemailer.createTransport({host: 'smtp.gmail.com', port: 465, secure: true, auth: {user: 'hashthe13@gmail.com', pass: 'hopjdkrlljqeduyy'}});
            transporter.sendMail({from: '"ReRAC" <hashthe13@gmail.com>', to: email, subject :"ReRAC Password Resetted", text: `Hi ${username},\n\n Your password has been resetted succesfully.\n\nCheears,\nReRAC Teams.`});

            res.redirect('/');
        });
    } else {res.redirect('/reset-password');}
});

// ----------------------------------- //

// Start at Port 3000

app.listen(3000, () => {
    console.log('Server listening on port 3000');
});
