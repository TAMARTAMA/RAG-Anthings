// מודל משתמשים
const mongoose = require('mongoose')
const UserSchema = new mongoose.Schema({
  userId: {
    type: String,
    required: true,
    unique: true,
    trim: true
  },
  rfidTag: {
    type: String,
    required: true,
    unique: true,
    trim: true
  },
  fullName: {
    type: String,
    required: true,
    trim: true
  },
  age: {
    type: Number,
    required: true,
    min: 3,
    max: 120
  },
  height: {
    type: Number,
    required: true,
    min: 90,
    max: 250
  },
  emergencyPhone: {
    type: String,
    required: true,
    trim: true,
    validate: {
      validator: function(v) {
        return /^[0-9\-\+\s\(\)]+$/.test(v);
      },
      message: 'Emergency phone number is not valid'
    }
  },
  registrationDate: {
    type: Date,
    default: Date.now,
    required: true
  }
}, {
  timestamps: true,
  collection: 'users'
});
module.exports = mongoose.model("User", UserSchema)