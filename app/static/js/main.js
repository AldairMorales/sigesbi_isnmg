const getTitleMessageFromCategory = category => {
    const titles = {
        'success': 'Ingreso Correcto!',
        'warning': 'Atención!',
        'info': 'Registro Correcto!',
        'delete': 'Eliminado!',
        'error': 'Oops...!'
    }
    return titles[category]
}
function showMessageAlert(category, message){
    Swal.fire({
        icon: category,
        title: getTitleMessageFromCategory(category),
        text: message
    })
}

