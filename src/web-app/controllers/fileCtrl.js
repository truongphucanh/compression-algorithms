var multer	=	require('multer');
var url = require('url');
var fs = require('fs');
var Promise = require('promise');
var exec = require('child_process').exec;
var base64Img = require('base64-img');
var path = require('path');
var mkdirp = require('mkdirp');
var decompress = require('decompress');
var Jimp = require("jimp");
const config = require('../config.json');

var createFolder = function() {
  return new Promise(function (resolve, reject) {

    var folderID = Date.now();
    var folderPath = config.uploadImgPath + folderID + "/";
    var command = "mkdir " + folderPath + " && chmod o+rw -R " + folderPath

    console.log("This is command");
    console.log(command);

    child = exec(command, function (err, stdout, stderr) {
      if (err)
        reject(err);

      resolve({
        file: "",
        folderID: folderID,
        folderPath: folderPath
      });
    })
  })
}

var convertBase64Img = function(pathInfo, strBase64) {
  return new Promise(function (resolve, reject) {
    base64Img.img(strBase64, pathInfo.folderPath, 'out', function(err, resultPath) {
      if (err)
        reject(err);
      pathInfo.file = resultPath;
      resolve(pathInfo);
    });    
  })
}

var streamImg = function(req, res, pathInfo) {
  // streaming img and save into file.
  console.log("This is streaming image file.");

  var storage	=	multer.diskStorage({
    destination: function (req, file, callback) {
      callback(null, pathInfo.folderPath);
    },
    filename: function (req, file, callback) {
      console.log("this is file name");
      console.log(file.originalname);
      var newFile = file.originalname;
      pathInfo.file = path.join(pathInfo.folderPath, file.originalname);
      callback(null, newFile);
    }
  });

  var upload = multer({ storage : storage }).array('userPhoto');

  return new Promise(function (resolve, reject) {
	  upload(req,res,function(err) {
		  if(err) reject(err);
      resolve(pathInfo);
    })

  })

}

var preProcessingImg = function(pathInfo, params) {
  return new Promise(function (resolve, reject) {
    console.log("This is pre processing img");
    console.log(pathInfo.file);

    if (params.convertImg != "true") {
      console.log("Do nothing preprocessing.")
      resolve(pathInfo);
      return;
    }
    
    Jimp.read(pathInfo.file).then(function (img) {

      if (params.width && params.height) {        
        img = img.resize(parseInt(params.width), parseInt(params.height))
      }

      if (params.quality) {
        img = img.quality(parseInt(params.quality));
      }

      var parser = path.parse(pathInfo.file);
      var extImg = parser.ext;

      if (params.fileType) {
        extImg = "." + params.fileType;
      }

      var saveFile = path.join(pathInfo.folderPath, parser.name + extImg);
      console.log(saveFile);
      pathInfo.file = saveFile;

      img.write(saveFile, function(err) {
        reject(err);
      });

      resolve(pathInfo);      

    }).catch(function (err) {
      reject(err)
    });    
    
  })
}


var getImage = function(req, res) {
  var folderID = req.params.folderid;
  var fileName = req.params.filename
  var pathFile;

  if (folderID == "oxford") {
    pathFile = path.join(config.oxfordPath, fileName);
  }
  else {
    pathFile = path.join(config.uploadImgPath, folderID + "/" + fileName)
  }


  if (!fs.existsSync(pathFile)) {
    return res.status(404).send('Your image not found.');
  }

  res.sendFile(pathFile);
}

var uploadImage = function(req, res) {
  var query = url.parse(req.url, true).query;

  createFolder().then(function(pathInfo) {
    return streamImg(req, res, pathInfo);

  }).then(function(pathInfo) {
    return preProcessingImg(pathInfo, req.body);

  }).then(function(pathInfo) {
    console.log("Uploaded file successfully.");

    if (query.algorithm == "runlength")    
      var command = "python compression-algorithms/src/runlength.py --input " +
        pathInfo.file + " --operation " + query.operation;
    else if (query.algorithm == "shannon")
      var command = "python compression-algorithms/src/shannonfano.py --input " +
          pathInfo.file + " --operation " + query.operation;
    else if (query.algorithm == "jpeg")
      var command = "python compression-algorithms/src/jpeg.py --input " +
          pathInfo.file + " --operation " + query.operation;

    console.log("this is command");
    console.log(command);
    
    child = exec(command, function (err, stdout, stderr) {
      if (err) {
        console.log("Err: ", err);
      }
      else {
        res.send("Do it ok.");
      }
    });

  }).catch(function(err) {
    console.error(err);
    res.status(422).send({
      msg: "Can not process base64 code or internal issues."
    });
  })

}

var uploadZip = function(req, res) {
  var today = new Date();
  var id = today.getFullYear() + "-" + (today.getMonth()+1) + "-" + today.getDate() + "-" + today.getHours() + "-" + today.getMinutes() + "-" + today.getSeconds();
  var folderPath = path.join(config.galleryPath, id);

  var oldmask = process.umask(0);
  mkdirp(folderPath, '0777', function(err) {
    process.umask(oldmask);
    if (err) {
      console.error(err)
      return res.status(422).send({
        msg: "Upload file failed, please contact to Admin."
      });
    }
    var pathInfo = {
      file: "",
      folderPath: folderPath
    }

    streamImg(req, res, pathInfo).then(function(pathInfo) {

      console.log("Uploaded file successfully.");
      var pathFile = path.join(pathInfo.folderPath, pathInfo.file);
      // return decompress(pathFile, pathInfo.folderPath, {strip: 1})
      return decompress(pathFile, pathInfo.folderPath);

    }).then(function(file) {

      console.log("Decompress file complete.");
      res.status(200).send({
        fileName: path.basename(pathInfo.file),
        fileID: id,
        msg: "Uploaded file successfully."
      });

    }).catch(function(err) {

      console.error(err);
      res.status(422).send({
        msg: "Upload file failed, please contact to Admin."
      });

    })

  });

}

module.exports = {
  getImage: getImage,
  uploadImage: uploadImage,
  preProcessingImg: preProcessingImg,
  uploadZip: uploadZip
}
  
