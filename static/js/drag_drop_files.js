
var dragHandler = function(evt) {
    evt.preventDefault();
    var files = evt.originalEvent.dataTransfer.files;

    var formData = new FormData();
    formData.append("file2upload", files[0]);

    var req = {
        url: "/document",
        method: "post",
        processData: false,
        contentType: false,
        data: formData
    };
    var promise = $.ajax(req);
};

var dropHandler = function(evt){
    evt.preventDefault();
    var files = evt.originalEvent.dataTransfer.files;
    console.log(files[0]);
};

var dropHandlerSet = {
    dragover: dragHandler,
    drop: dropHandler
};

$(".droparea").on(dropHandlerSet);

