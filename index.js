const path =require('path');
const mongoose = require('mongoose');
const patients = require('../models/patients');

mongoose.connect('mongodb://localhost:27017/PREDICTOR',{
    
});
const db = mongoose.connection;
db.on("error", console.error.bind(console,"connection error:"));
db.once("open",() => { 
    console.log("database connected");
});

const seedDB = async () =>{
    await patients.deleteMany({});
    const pat =new patients({
        name:'Manav Singh',
        age:18, 
        gender:'Male',
        file:''
        
    })
await pat.save()
}
seedDB();
