$(document).ready(function () {
  //? Prevent default drag behaviors
  $("#upload-file").on("dragenter dragover", function (event) {
    event.preventDefault();
  });

  //? Handle dropped files
  $("#upload-file").on("drop", function (event) {
    event.preventDefault();

    var files = event.originalEvent.dataTransfer.files;
    $("#uploaded-file").html(
      "<h3> File Selected Successfully. Click on upload to procced</h3>"
    );
    displayFiles(files);
  });

  function displayFiles(files) {
    var fileList = $("#upload")[0].files;
    var newFileList = new DataTransfer();
    for (var i = 0; i < fileList.length; i++) {
      newFileList.items.add(fileList[i]);
    }
    for (var i = 0; i < files.length; i++) {
      newFileList.items.add(files[i]);
    }
    $("#upload")[0].files = newFileList.files;
  }

  //? Handle file input change event
  $("#upload").change(function () {
    var files = $(this)[0].files;
    displayFiles(files);
  });

  //? Trigger file input click event when upload area is clicked
  $("#upload-file").click(function () {
    $("#upload").click();
  });
});
