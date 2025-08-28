// Simulated messages array
const messages = [
  { userId: 'testUser', message: 'Hello, how can I help you?' },
  { userId: 'testUser', message: 'This is a simulated response.' },
  { userId: 'testUser', message: 'Your request has been received.' }
];

const giveResponse = (req, res) => {
  try {
    const { userId, requset } = req.body;
    if (!userId || requset === undefined)
      return res.status(400).json({ error: "Missing fields" });

    // Simulate sending a message from the array (random or first)
    const responseMsg = messages[Math.floor(Math.random() * messages.length)].message;
    res.status(200).json({ message: responseMsg });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
module.exports = { giveResponse };