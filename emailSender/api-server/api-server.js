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

app.post('/api/email', async (req, res) => {
  const { to, subject, text, emailUser, emailPass } = req.body;

  if (!emailUser || !emailPass) {
    return res.status(400).json({ error: "Email credentials required" });
  }

  try {
    await emailQueue.add({
      from: emailUser,        // use emailUser as from
      to,
      subject,
      text,
      emailUser,
      emailPass,
    }, {
      attempts: 5,
      backoff: { type: 'exponential', delay: 3000 },
    });

    res.status(200).json({ message: 'Email queued for sending' });
  } catch (error) {
    res.status(500).json({ error: 'Failed to queue email', message: error.message });
  }
});



const PORT = process.env.PORT || 3020;
app.listen(PORT, () => console.log(`API listening on port ${PORT}`));
