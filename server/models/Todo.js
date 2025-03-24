const mongoose = require("mongoose");
const TodoSchema = new mongoose.Schema(
  {
    task: { type: String, required: true },
    done: { type: Boolean, default: false },
  },
  { collection: "todos" }
);
const TodoModel = mongoose.model("todos", TodoSchema);
module.exports = TodoModel;
