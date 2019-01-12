import MicroModal from 'micromodal'

console.dir(MicroModal)
MicroModal.init();

const btn = document.querySelector('#btn');
btn.addEventListener('click', () => {
    MicroModal.show('addEleModal');
})

const kindSelector = document.querySelector('#kind')

kindSelector.addEventListener('change', (e) => {
    const pathInput = document.querySelector('#path')

    const value = e.target.value
    if(value === "1"){
        pathInput.placeholder = 'name'
    }else{
        pathInput.placeholder = 'url format'

    }
})

const submitEleBtn = document.querySelector('#submit')

submitEleBtn.addEventListener('click', () => {
    document.querySelector('#addEleForm').submit()
})

const categoryLis = document.querySelectorAll('.category')
categoryLis.forEach(function(ele){
    ele.addEventListener('click', function () {
        const url  = this.dataset.href

        location.href = url
    })
})

const bookMakrkLis = document.querySelectorAll('.bookmark')
bookMakrkLis.forEach(function(ele){
    ele.addEventListener('click', function () {
        const changeIdHidden = document.querySelector('#changeThumbnail #change_id')
        changeIdHidden.value = this.dataset.id

        const thumbnailFInpit = document.querySelector('#thumbnail')
        thumbnailFInpit.value = ''
        MicroModal.show('changeThumbnail');

    })

})

const changeEleBtn = document.querySelector('#change')
changeEleBtn.addEventListener('click', () => {
    document.querySelector('#changeThumbNailForm').submit()
})