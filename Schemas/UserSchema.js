var mongoose = import('mongoose');
var Schema = mongoose.Schema;

var userSchema = new Schema({
    companyName: String,
    //Personal Information
    firstName: String,
    lastName: String,
    age: Number,
    birthDate: String,
    jobTitle: String,
    //Account Info
    userName: String,
    email: String,
    dateCreated: String,
    validationStatus: Boolean,
    lastLogin: String,
    devicesLoggedIn: [{ device: String, loginDate: String }],
    //Password Stuff
    password: String,
    passwordSalt: String,
    passwordHints: [{ hint: String, ans: String }]
});