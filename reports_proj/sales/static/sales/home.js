//console.log('hello world tests')

const reportBtn = document.getElementById("report-btn")
const img = document.getElementById("img")
const modalBody = document.getElementById('modal-body')

//console.log(img)
//console.log(reportBtn)

const reportName = document.getElementById('id_name')
const reportRemarks = document.getElementById('id_remarks')
//console.log(reportName)
//console.log(reportRemarks)

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
//console.log(csrf)

const reportForm = document.getElementById('report-form')
//console.log(reportForm)

const alertBox = document.getElementById('alert-box')

const handleAlerts = (type, message) => {
        alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${message}
        </div>
    `
}

if (img){
    reportBtn.classList.remove('not-visible')
}

reportBtn.addEventListener('click', ()=>{
    console.log('clicked')
    img.setAttribute('class', 'w-100')
    modalBody.prepend(img)



    reportForm.addEventListener('submit', (e)=>{
        e.preventDefault();
        const formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrf)
        formData.append('name', reportName.value)
        formData.append('remarks', reportRemarks.value)
        formData.append('image', img.src)

        $.ajax({
            type: 'POST',
            url: '/reports/save/',
            data: formData,
            success: function(response){
                handleAlerts('success', 'report created')
                                reportForm.reset()

            },
            error: function(error){
                handleAlerts('danger', 'oops... something went wrong!')
            },
            processData: false,
            contentType: false,
        })
    })

})