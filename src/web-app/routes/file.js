var express = require('express');
var fileCtrl = require('../controllers/fileCtrl');

var router = express.Router();

router.route('/image/:folderid/:filename').get(fileCtrl.getImage);
router.route('/image').post(fileCtrl.uploadImage);
router.route('/zip').post(fileCtrl.uploadZip);

module.exports = router;
