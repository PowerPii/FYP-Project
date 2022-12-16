const express = require('express');
var bodyParser = require('body-parser');
const connection = require('./database')

// App Configuration

const app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Admin

// Handle GET request

app.get('/admin/get', (req, res) => {
    const request = req.query.request;
    const database = req.query.database;

    if (request == "ALL") {
        connection.query(`SELECT * FROM application.${database}`, (error, results) => {
            if (error) {throw error}
            console.log(results)
            res.send(results);
        });
    }
    else {
        res.sendStatus(404);
    }
});
    
// Handle POST request

app.post('/admin/post', (req, res) => {
    const request = req.body.request;
    const database = req.body.database;
    const data = req.body.data;

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
            let date = data.date;
            let time = data.time;
            let service_no = data.service_no;
            let arrival_time = data.arrival_time;
            let latitude = data.latitude;
            let longitude = data.longitude;

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

app.listen(3000, () => {
    console.log('Server listening on port 3000');
});
