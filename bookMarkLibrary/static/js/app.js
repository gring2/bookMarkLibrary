import MicroModal from 'micromodal'


MicroModal.init();

const btn = document.querySelector('#btn');
btn.addEventListener('click', () => {
    MicroModal.show('addEleModal');
})


const submitEleBtn = document.querySelector('#submit')

submitEleBtn.addEventListener('click', () => {
    const submitEvent = new Event('submit')

    document.querySelector('#addEleForm').dispatchEvent(submitEvent)
})


const bookMakrkLis = document.querySelectorAll('.bookmark')
bookMakrkLis.forEach(function(ele){
    ele.addEventListener('contextmenu', function () {
        const changeIdHidden = document.querySelector('#changeThumbnail #change_id')
        changeIdHidden.value = this.dataset.id

        const thumbnailFInpit = document.querySelector('#thumbnail')
        thumbnailFInpit.value = ''
        MicroModal.show('changeThumbnail');

    })
    ele.addEventListener('click', function(){
        const url = this.dataset.url
        const child = window.open(url, '_blank');
        child.focus()
    })
})

const addEleForm = document.querySelector('#addEleForm')
addEleForm.addEventListener('submit', () => {
    const HASH = '#'
    const tagsEl = document.querySelector('#addEleForm > #tags')
    let tagsVal = tagsEl.value === '' ?[]: [...new Set(tagsEl.value.split(HASH).map(tag => tag.trim()))]
    tagsEl.value = tagsVal
    document.querySelector('#addEleForm').submit()
})