function validateImageSearchForm() {
  var fileInput = jQuery('#listFile');
  var input = fileInput.get(0);
  
  if (!input.files.length) {
    alert('Please upload a file before continuing')
    return false;
  }

  var fileGroupName = jQuery("#listFile").val().split("\\").pop().replace("_", " ").match(/("[^"]+"|[^"\s]+)/g)[0];

  var operation = jQuery("#operation").val();
  var algorithm = jQuery("#algorithm").val();
  
  console.log(fileGroupName);

  jQuery('#uploadForm').attr("action", "/v1/file/image?method=stream" + "&project=" + "imageRetrieval" + "&operation=" + operation + "&algorithm=" + algorithm);
  
  return true;
}
