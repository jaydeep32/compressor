

// quality = document.getElementById('quality')
cancel = document.querySelector('#cancel')


function upload(){
        Dropzone.autoDiscover = false
        globalThis.myDropzone = new Dropzone('#my-dropzone', {
            url: '/file_upload',
            timeout: 600000,
            dictDefaultMessage: "Drop your file here to upload...",
            init: function(){
                this.on('sending', function(file, xhr, formData){
                    // formData.append('csrfmiddlewaretoken', csrftoken)
                    // formData.append('quality', quality.value)
                });
                this.on("success", function (file, response) {
                    console.log("sucesso");
                    console.log(response)
                    window.location.href = `/download_file/${response.filename}`;
                });
                this.on("error", function (file, response) {
                    console.log(response);
                });
            },
            // maxFiles: 1,
            clickable: [".fileinput-button", "#my-dropzone"],
            // chunking: true,
            //maxFilesize: 4,
            //acceptedFiles: '.png, .jepg, .jpg'
        })
    }

upload()

// $(quality).change(function(){
//     if (myDropzone.files.length >= 1){
//         upload()
//     }
// })
    
cancel.addEventListener('click', () => {
    // console.log("click")
    myDropzone.removeAllFiles( true );
});


const progress = document.querySelector('.progress-done');

setTimeout(() => {
  progress.style.opacity = 1;
  progress.style.width = progress.getAttribute('data-done') + '%';
}, 500)


