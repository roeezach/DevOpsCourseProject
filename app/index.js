const express = require("express");
const app = express();
const path = require("path");

// Middleware to parse form data
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));

// Currency conversion rates
const rates = {
  usd: 0.27,
  eur: 0.25,
  gbp: 0.21
};

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.post("/convert", (req, res) => {
  const shekels = parseFloat(req.body.shekels);
  const target = req.body.currency;
  const rate = rates[target] || 0;
  const converted = (shekels * rate).toFixed(2);
  const symbols = { usd: "$", eur: "€", gbp: "£" };
  const symbol = symbols[target] || "?";

  res.send(`
    <html>
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="stylesheet" href="/style.css">
        <title>Conversion Result</title>
      </head>
      <body>
        <div class="container">
          <h2 id="result">₪${shekels} = ${symbol}${converted}</h2>
          <button id="convert-again" onclick="window.location.href='/'">Convert Again</button>
        </div>
      </body>
    </html>
  `);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));