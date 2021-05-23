//console.log('hello world tests')

const reportBtn = document.getElementById("report-btn")
const img = document.getElementById("img")
const modalBody = document.getElementById('modal-body')

console.log(img)
console.log(reportBtn)

if (img){
    reportBtn.classList.remove('not-visible')
}

reportBtn.addEventListener('click', ()=>{
    console.log('clicked')

})