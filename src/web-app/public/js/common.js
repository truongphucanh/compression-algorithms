function msg(type, message) {
  jQuery.notify(
    message,
    {
      className: type,
      position:"bottom center" }
  );
}

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      jQuery("#downloadImg").attr("href", e.target.result);
      /*pannellumOptions.panorama = e.target.result;
       *pannellum.viewer('panorama', pannellumOptions);*/
    }

    reader.readAsDataURL(input.files[0]);
  }
}

function onFileSelected(event) {
  var selectedFile = event.target.files[0];
  var reader = new FileReader();

  console.log('go here');

  var imgtag = document.getElementById("originalImg");
  imgtag.title = selectedFile.name;

  reader.onload = function(event) {
    imgtag.src = event.target.result;
  };

  reader.readAsDataURL(selectedFile);
}
