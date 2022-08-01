const functions = require("firebase-functions");
const express = require("express");

const app = express();

// catch all
app.all("*", (req, res) => {
  res.send("hii");
});

exports.app = functions.https.onRequest(app);
