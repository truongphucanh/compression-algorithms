var app = angular.module('starter', []);

var initAll = function($scope) {
  $scope.selected = {};
  $scope.predictResult = "Không có";
  $scope.statusResult = {
    showMsg: "No execution",
    hideMsg: "No execution"
  };
}

app.controller('myCtrl', function($scope) {

  initAll($scope);

  console.log("this is angular");
  console.log(JSON.stringify($scope.dataset));

  $scope.renderMainFrameImage = function(listResult) {

    var htmlCode = "<ul id='image-gallery' class='gallery list-unstyled cS-hidden'>";

    listResult.forEach(function(item) {
      htmlCode = htmlCode + "<li data-thumb='" + item + "'>" + "<img src='" + item +"' width='766px' height='500px'/></li>"
    })

    htmlCode = htmlCode + "</ul>";

    console.log("This is html code");
    console.log(htmlCode);
    jQuery("#mainFrameImage").html(htmlCode);

  };

  $scope.listResult = []

  $scope.title = "segmentation";
  $scope.menuClassTab = {
    segmentation: function() {
      jQuery("#segmentationTab").attr("class", "active item");
      jQuery("#imagesearchTab").attr("class", "item");
    },
    imagesearch: function() {
      jQuery("#segmentationTab").attr("class", "item");
      jQuery("#imagesearchTab").attr("class", "active item");
    }    
  }
  $scope.chooseTitle = function(value) {
    console.log('this is your value');
    console.log(value);
    $scope.menuClassTab[value]();
    $scope.title = value;
  };

  $scope.findResult = function() {
    var result = predictResultByTree(classifyTree, $scope.selected)
    console.log(result);
    if (result) {
      $scope.predictResult = result.Value;
      $scope.statusResult = {
        showMsg: "Thành công",
        hideMsg: "Không có lỗi"
      };
    }
    else {
      $scope.predictResult = "Không có kết quả";
      $scope.statusResult = {
        showMsg: "Có lỗi",
        hideMsg: "Có lỗi hoặc không tìm thấy. Xem lại câu truy vấn."
      };
    }
    
  }

  $scope.changeSelectedItem = function(key, value) {
    $scope.selected[key] = value;
    console.log('what value is')
    console.log(value)
    console.log($scope.selected);
  }

  $scope.clearAll = function() {
    initAll($scope);
  }

  $scope.myfunction = function (data) {
    console.log('can go myfunction')
    console.log(JSON.stringify(data.listAttribute))
    $scope.listAttribute = data.listAttribute;
    $scope.$apply();
  };
})

app.directive('intro', function() {
  return {
    restrict: 'E',
    scope: {
      options: '=',
    },
    templateUrl: 'view/intro.html',
    link: function() {
      jQuery('#intro').click(function () {
        jQuery('.ui.modal')
          .modal('show');
      });
    }
  };
});

app.directive('rendersegmentation', function() {
  return {
    restrict: 'E',
    transclude: true,
    scope: {
      options: '=',
    },
    templateUrl: 'view/segmentation.html',
    link: function(scope, element, attrs) {
      console.log('This is segmentation');
      initAll(scope);

      jQuery("#downloadImg").attr("href", "pic/sample.jpg");

      jQuery('#uploadForm').submit(false);
      jQuery('#uploadForm').submit(function() {
		    jQuery("#status").empty().text("File is uploading...");
        jQuery("#status").attr("data-tooltip", "Executing");
        jQuery("#status").attr("class", "ui blue label");

        console.log('This is upload form');
        jQuery(this).ajaxSubmit({

          error: function(xhr) {
            console.log('This is error');
		        /*status('Error: ' + xhr.status);*/
            var errorMsg = "Error in processing"
            var errDescription = "Something error happening in Server"

		        jQuery("#status").empty().text(errorMsg);
            jQuery("#status").attr("data-tooltip", errDescription);
            jQuery("#status").attr("class", "ui red label");

          },

          success: function(response) {
            console.log('This is success');
		        var id = response;
            console.log('This is your id');
            console.log(id);
            var resultImg = "/uploads/" + id;

            var imgtag = document.getElementById("segmentedImg");
            imgtag.src = resultImg;
            
            jQuery("#downloadImg").attr("href", resultImg);

		        jQuery("#status").empty().text("Completed");
            jQuery("#status").attr("data-tooltip", "No error");
            jQuery("#status").attr("class", "ui green label");

            jQuery("#container1").twentytwenty();

          }
	      });

      });


    }
  };
});

app.directive('renderimagesearch', function() {
  return {
    restrict: 'E',
    transclude: false,
    scope: false,
    templateUrl: 'view/imagesearch.html',
    link: function(scope, element, attrs) {
      console.log('This is image search');
      initAll(scope);

      jQuery('#uploadForm').submit(false);
      jQuery('#uploadForm').submit(function() {
		    jQuery("#status").empty().text("File is uploading...");
        jQuery("#status").attr("data-tooltip", "Executing");
        jQuery("#status").attr("class", "ui blue label");

        console.log('This is upload form');
        jQuery(this).ajaxSubmit({

          error: function(xhr) {
            console.log('This is error');
		        /*status('Error: ' + xhr.status);*/
            var errorMsg = "Error in processing"
            var errDescription = "Something error happening in Server"

		        jQuery("#status").empty().text(errorMsg);
            jQuery("#status").attr("data-tooltip", errDescription);
            jQuery("#status").attr("class", "ui red label");

          },

          success: function(response) {

		        jQuery("#status").empty().text("Completed");
            jQuery("#status").attr("data-tooltip", "No error");
            jQuery("#status").attr("class", "ui green label");

            console.log('This is success');
		        var id = response;
            console.log('This is your id');
            console.log(id);

            jQuery.ajax({
              url: "/getResultList?folderID=" + id,
            }).done(function(res) {
              console.log(res);
              console.log("this is listresult original");
              console.log(JSON.stringify(scope.listResult));

              scope.$apply(function(){
                scope.listResult = JSON.parse(res);
              });

              scope.renderMainFrameImage(scope.listResult);

              jQuery('#image-gallery').lightSlider({
                gallery:true,
                item:1,
                thumbItem:9,
                slideMargin: 0,
                speed:500,
                auto:true,
                loop:true,
                onSliderLoad: function() {
                  jQuery('#image-gallery').removeClass('cS-hidden');
                }  
              });

              console.log('This is frist one');
              console.log(scope.listResult[0]);
            });




          }
	      });

      });


    }
  }

});
