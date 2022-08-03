const functions = require("firebase-functions");
const express = require("express");
const admin = require("firebase-admin");

const todo_app = express();

// todo api
// add new todo
// edit/update a todo
// delete a todo

admin.initializeApp({
  databaseURL:
    "https://tutorial-6839b-default-rtdb.asia-southeast1.firebasedatabase.app/"
});

todo_app.post("/addNewTodo", async (req, res) => {
  if (req.query.title == undefined || req.query.note == undefined) {
    return res.json({
      ok: false
    });
  }
  await admin.firestore().collection("todo").add({
    title: req.query.title,
    note: req.query.note,
    completed: false
  });
  return res.json({
    ok: true
  });
});

todo_app.post("/getTodo", async (req, res) => {
  const todo_id = req.query.todo_id;
  if (todo_id == undefined) {
    return res.json({
      ok: false
    });
  }
  try {
    var todo = await admin.firestore().collection("todo").doc(todo_id).get();
    if (todo.exists) {
      return res.json(todo.data());
    }
  } catch (e) {
    console.log(e.message);
    return res.json({
      ok: false
    });
  }
  return res.json({
    ok: true
  });
});

todo_app.post("/getAllTodos", async (req, res) => {
  var docs = await admin.firestore().collection("todo").get();
  var new_docs = [];
  docs.forEach((doc) => {
    var data = doc.data();
    data["id"] = doc.id;
    new_docs.push(data);
  });
  return res.json({
    ok: true,
    data: new_docs
  });
});

todo_app.post("/deleteTodo", async (req, res) => {
  const todo_id = req.query.todo_id;
  if (todo_id == undefined) {
    return res.json({
      ok: false
    });
  }
  try {
    await admin.firestore().collection("todo").doc(todo_id).delete();
  } catch (e) {
    console.log(e);
    return res.json({
      ok: false,
      msg: e.message
    });
  }
  return res.json({
    ok: true,
    msg: "todo was deleted"
  });
});

todo_app.post("/deleteAllTodos", async (req, res) => {
  var docs = await admin.firestore().collection("todo").get();
  docs.forEach(async (doc) => {
    await admin.firestore().collection("todo").doc(doc.id).delete();
  });
  return res.json({
    ok: true
  });
});

todo_app.post("/setAsComplete", async (req, res) => {
  const todo_id = req.query.todo_id;
  if (todo_id == undefined) {
    return res.json({
      ok: false
    });
  }
  await admin.firestore().collection("todo").doc(todo_id).update({
    completed: true
  });
  return res.json({
    ok: true
  });
});

// catch all
todo_app.all("*", (req, res) => {
  res.send("whatever ur looking for is not here");
});

exports.app = functions.https.onRequest(todo_app);

// auth triggers

exports.userCreated = functions.auth.user().onCreate((user) => {
  console.log(user);
});

exports.userDeleted = functions.auth.user().onDelete((user) => {
  console.log(user);
});

exports.onUserDocumentCreate = functions.firestore
  .document("users/{docId}")
  .onCreate((snapshot, context) => {
    console.log(snapshot.data());
  });
