const mongoose = require("mongoose");

const EmployeeSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
  },
  { collection: "employesses" } // Ensure this matches exactly with MongoDB
);

const EmployeeModel = mongoose.model("employesses", EmployeeSchema); // Ensure this matches
module.exports = EmployeeModel;
