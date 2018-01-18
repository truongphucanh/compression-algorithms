function validateSegmentForm() {
  var fileInput = jQuery('#listFile');
  var input = fileInput.get(0);
  var kNumber = jQuery('#kNumber').val();

  if (!kNumber) {
    alert('Please input k number')
    return false;         
  }
  
  if (!input.files.length) {
    alert('Please upload a file before continuing')
    return false;
  }

  jQuery('#uploadForm').attr("action", "/api/photo?knumber=" + kNumber + "&project=" + "segmentation");
  
  return true;
}
