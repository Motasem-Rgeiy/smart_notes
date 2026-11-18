const create_btn = document.getElementById('create-btn');
    const create_options = document.getElementById('create-options');


create_btn.addEventListener('click' ,() => {
    

    create_options.classList.remove('hidden');
    create_options.classList.add('flex');
    
})

const close_btn = document.getElementById('close-btn');

close_btn.addEventListener('click' , () => {
    create_options.classList.remove('flex');
    create_options.classList.add('hidden');
})
