var dragHandler = function(evt) {
            evt.preventDefault();
        };

var dropHandler = function(evt){
    evt.preventDefault();
    var files = evt.originalEvent.dataTransfer.files;

    var formData = new FormData();
    formData.append("file2upload", files[0]);

    $.ajax({
        url: "/document/upload_file",
        method: "post",
        processData: false,
        contentType: false,
        data: formData,
        success: function(data) {
            $('.message').text('').append(data);
            console.log(data)

        }
    });

    console.log(files[0].name);
};

var dropHandlerSet = {
    dragover: dragHandler,
    drop: dropHandler
};

$('.droparea').on(dropHandlerSet);

