import MicroModal from 'micromodal'


MicroModal.init();

const btn = document.querySelector('#btn');
btn.addEventListener('click', () => {
    MicroModal.show('addEleModal');
})


const submitEleBtn = document.querySelector('#submit')

submitEleBtn.addEventListener('click', () => {
    document.querySelector('#addEleForm').submit()
})


const bookMarkList = document.querySelectorAll('.bookmark')
bookMarkList.forEach(function(ele){
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

