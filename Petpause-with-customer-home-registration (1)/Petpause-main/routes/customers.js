// Public customer registration and booking-request endpoints.
const express = require('express');
const crypto = require('crypto');
const db = require('../db/database');
const passwords = require('../lib/passwords');
const check = require('../lib/check');
const dates = require('../lib/dates');
const router = express.Router();

router.post('/register', (req, res) => {
  const fullName = check.str(req.body.fullName);
  const email = check.str(req.body.email).toLowerCase();
  const phone = check.str(req.body.phone);
  const password = typeof req.body.password === 'string' ? req.body.password : '';
  const password2 = typeof req.body.password2 === 'string' ? req.body.password2 : '';
  if (!fullName || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !check.phone(phone)) {
    return res.status(400).json({error:'Enter your name, a valid email address and a 10-digit phone number.'});
  }
  const issue = passwords.checkStrength(password, email);
  if (issue) return res.status(400).json({error:issue});
  if (password !== password2) return res.status(400).json({error:'Passwords do not match.'});
  const salt = crypto.randomBytes(16).toString('base64');
  try {
    db.prepare('INSERT INTO customers (full_name,email,phone,password_hash,salt,created_at) VALUES (?,?,?,?,?,?)')
      .run(fullName,email,phone,passwords.hash(password,salt),salt,dates.nowText());
    res.json({message:'Your customer account has been created. You can now submit a booking request.'});
  } catch (e) {
    if (String(e.code).includes('SQLITE_CONSTRAINT')) return res.status(409).json({error:'An account with this email already exists.'});
    throw e;
  }
});

router.post('/booking-request', (req,res) => {
  const email = check.str(req.body.email).toLowerCase();
  const password = typeof req.body.password === 'string' ? req.body.password : '';
  const c = db.prepare('SELECT * FROM customers WHERE email=?').get(email);
  if (!c || !passwords.matches(password,c.salt,c.password_hash)) return res.status(401).json({error:'Email or password is incorrect.'});
  const petName = check.str(req.body.petName), breed = check.str(req.body.breed);
  const start = dates.parse(check.str(req.body.startDate)), end = dates.parse(check.str(req.body.endDate));
  if (!petName || !breed || !start || !end || start < dates.today() || end <= start) {
    return res.status(400).json({error:'Enter your pet details and valid dates. The end date must be after the start date and the start date cannot be in the past.'});
  }
  const id = db.prepare(`INSERT INTO customer_booking_requests
    (customer_id,pet_name,pet_breed,start_date,end_date,notes,created_at) VALUES (?,?,?,?,?,?,?)`)
    .run(c.id,petName,breed,start,end,check.str(req.body.notes),dates.nowText()).lastInsertRowid;
  res.json({message:`Booking request #${id} has been submitted. PetPause staff will confirm availability with you.`});
});
module.exports = router;
