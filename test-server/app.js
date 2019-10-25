const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.get('/', (req,res) => {
    res.send('Send me a JSON!');
});

app.post('/', (req,res) => {
    res.json(req.body);
    console.log(req.body);
});

app.listen(port, () => console.log(`Example app listening on port ${port}!`))