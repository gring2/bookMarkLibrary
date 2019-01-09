import MicroModal from 'micromodal'

console.dir(MicroModal)
MicroModal.init();

const btn = document.querySelector('#btn');
btn.addEventListener('click', () => {
    MicroModal.show('addEleModal');
})