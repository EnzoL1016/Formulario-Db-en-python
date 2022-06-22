const deleteButton = document.querySelectorAll('.deleteButton')

if(deleteButton){
    const buttonArray = Array.from(deleteButton);
    buttonArray.forEach((button) => {
        button.addEventListener('click', (e) => {
            if(!confirm('Seguro que desea eliminar este paciente?')){
                e.preventDefault();
            }
        })
    })

}