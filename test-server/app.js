const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// get requests don't do anything
app.get('/', (req,res) => {
    res.send('Send me a JSON!');
});

// sends the response as a json object containing the request's data
app.post('/', (req,res) => {
    // res.json(req.body);
    console.log("Incoming: ", req.body);

    let testresults = {
        results:[
            {source:req.body.claim, link:req.body.link},
            {source:"test_source", link:"http://example.com/"}
        ]
    }

    res.json(testresults);
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`))