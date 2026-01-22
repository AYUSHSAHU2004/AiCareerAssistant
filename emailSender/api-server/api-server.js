const express = require('express');
const EmailGroup = require('./models/EmailGroup');
require('./db'); // connect to MongoDB

const Queue = require('bull');
const cors = require('cors');
const app = express();

app.use(cors());        app.use(express.json());


const emailQueue = new Queue('emailQueue', {
  redis: { host: process.env.REDIS_HOST, port: process.env.REDIS_PORT },
});



const PORT = process.env.PORT || 3020;
app.listen(PORT, () => console.log(`API listening on port ${PORT}`));
