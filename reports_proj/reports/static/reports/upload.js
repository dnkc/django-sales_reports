const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
// console.log(csrf)
const alertBox = document.getElementById('alert-box')

Dropzone.autoDiscover = false

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
}

const myDropzone = new Dropzone("#my-dropzone", {
    url: '/reports/upload/',
    init: function(){
        this.on('sending', function(file, xhr, formData){
            // console.log('sending')
            formData.append('csrfmiddlewaretoken', csrf)
        })
        this.on('success', function(file, response){
            const ex = response.ex
           if(response.ex) {
                handleAlerts('danger', 'File already exists!')
            } else {
                handleAlerts('success', 'Your file has been uploaded!')
            }
        })
    },
    maxFiles: 3,
    maxFilesize: 3, // 3 MB
    acceptedFiles: '.csv',
})