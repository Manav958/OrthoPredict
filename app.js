const express = require('express');
const { spawn } = require('child_process');
const app = express();
const port = 3000; // You can choose any port you prefer
const ejsMate = require ('ejs-mate');
const methodOverride = require('method-override');
const path =require('path');
const mongoose=require('mongoose');
const patients=require('./models/patients');
const bodyParser = require('body-parser');
const axios=require('axios');
mongoose.connect('mongodb://localhost:27017/PREDICTOR',{
    
});

const db = mongoose.connection;
db.on("error", console.error.bind(console,"connection error:"));
db.once("open",() => { 
    console.log("database connected");
});

app.engine('ejs'  , ejsMate)
app.set('view engine','ejs');
app.set('views',path.join(__dirname,'views'));
app.use(methodOverride('_method'))
app.use(express.urlencoded({extended:true}))
app.use('/', express.static(__dirname));
app.use('/predict/new', express.static(__dirname));
app.use('/predict', express.static(__dirname));
app.use('/patient_recover', express.static(__dirname));




app.get('/' ,(req,res)=> {
    res.render('home.ejs')
})

app.get('/predict' ,async (req,res)=> {
    const pat=await patients.find({})
    res.render('index.ejs', {pat})
});

app.get('/predict/new',(req,res)=>{
    res.render('new.ejs');
})

app.post('/predict',async (req, res) => {
    const pat = new patients(req.body.pat);
    await pat.save();
    res.redirect('/predict')
        
        
});




app.delete('/predict/:id',async(req,res)=>{
    const{id}=req.params;
    await patients.findByIdAndDelete(id);
    res.redirect('/predict');
});

app.get('/patient_recover',async(req,res)=>{
    const response=await axios.post('http://localhost:5000/predict');
    const a= response.data;
    
    res.render('show.ejs',{a})
    
});





    










app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
