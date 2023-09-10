const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const patientSchema = new Schema({
    name: String,
    age: Number,
    gender: String,
    file: String
    

});
module.exports = mongoose.model('patients', patientSchema);